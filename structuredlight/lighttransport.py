from typing import Tuple, List
import numpy as np
from .unstructured import Unstructured

class LightTransport(Unstructured):
    """Light Transport Matrix

    The Light Transport Matrix expresses the relationship 
    between the light source (e.g., projector) and the camera in linear form.
    It can represent as follows:
      c = Tp
    The column vector `p` is the projected pattern (pq, 1).
    The column vector `c` is the image captured by the camera (mn, 1).
    The matrix `T` is the light transport matrix (mn, pq).

    The light transport matrix is used for relighting[1] and dual-photography[2].

    The brute-force is the simplest method to acquire the light transport matrix, 
    capturing images by illuminating the light sources one by one in sequence. 
    The brute-force method is susceptible to sensor noise.

    This `LightTransport` class uses multiplexed illumination [3] to acquire the light transport matrix. 
    Multiple sources are illuminated in a single capture in the measurement, 
    and the matrix is estimated after capturing images.

    However, as you may have noticed, this method is highly time-consuming for capturing. 
    An efficient way to acquire the light transport matrix has been proposed [2][4][5]. 
    This `LightTransport` class does NOT support these efficient methods, but consider them if you want.
    
    References
    ----------
    .. [1] Debevec et al., "Acquiring the reflectance field of a human face." SIGGRAPH 2000.
    .. [2] Sen et al., "Dual photography." SIGGRAPH 2005.
    .. [3] Schechner et al., "A theory of multiplexed illumination." ICCV 2003.
    .. [4] Peers et al., "Compressive light transport sensing." TOG 2009.
    .. [5] Wang et al., "Kernel Nyström method for light transport." SIGGRAPH 2009.
    """

    def generate(self, dsize: Tuple[int, int], num: int) -> List[np.ndarray]:
        """
        Parameters
        ----------
        dsize : Tuple[int, int]
          pattern size
        num : int
          number of patterns

        Returns
        -------
        imlist : List[np.ndarray]
          generated patterns
        """
        frequencies = np.linspace(1, max(dsize)/2, num)
        imlist = [self._generate_unstructured_single(dsize, f) for f in frequencies]
        return imlist

    def decode(self, imlist_code: List[np.ndarray], imlist_observe: List[np.ndarray]) -> np.ndarray:
        """
        Parameters
        ----------
        imlist_code : List[np.ndarray]
          The projected patterns. 
          Image dsize is (q, p, cc).
          `p` and `q` correspondence to width and height.
          `cc` correspondence to color channel (gray: 1, rgb: 3).
        imlist_observe : List[np.ndarray]
          The images captured by the camera. image size is (n, m, co).
          Image dsize is (n, m, co).
          `n` and `m` correspondence to width and height.
          `co` correspondence to color channel (gray: 1, rgb: 3).

        Returns
        -------
        T : np.ndarray
          Light transport matrix (m*n*cc, p*q*co)
        """
        num = len(imlist_code) # = len(imlist_observe)

        pn = np.reshape(imlist_code, (num, -1)).T # (p*q*cc, num)
        cn = np.reshape(imlist_observe, (num, -1)).T # (m*n*co, num)
        
        # Calculate Light Transport Matrix
        pn_pinv = np.linalg.pinv(pn) # (num, p*q*cc)
        T = cn @ pn_pinv # (m*n*cc, p*q*co)
    
        return T
