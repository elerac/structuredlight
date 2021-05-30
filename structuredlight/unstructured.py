from typing import Tuple, List
import numpy as np
from .zncc import Zncc

class Unstructured(Zncc):
    """Unstructured Light
    
    Unstructured light pattern is proposed by Couture et al. [1].
    "This method featuring band-pass white noise patterns 
    that are designed to be robust to interreflections 
    by avoiding large black or white pattern regions."
    
    This class is based on Couture's method, 
    but there may be some differences.
    
    References
    ----------
    .. [1] Couture et al., "Unstructured light scanning to overcome interreflections." ICCV 2011.
    """

    def generate(self, dsize: Tuple[int, int], f: float, num: int) -> List[np.ndarray]:
        """
        Parameters
        ----------
        dsize : Tuple[int, int]
          pattern size
        f : float
          frequency
        num : int
          number of patterns

        Returns
        -------
        imlist : List[np.ndarray]
          generated patterns
        """
        imlist = [self._generate_unstructured_single(dsize, f) for _ in range(num)]
        return imlist

    @staticmethod
    def _generate_unstructured_single(dsize: Tuple[int, int], f: float) -> np.ndarray:
        """
        Parameters
        ----------
        dsize : Tuple[int, int]
          pattern size
        f : float
          frequency

        Returns
        -------
        img_unstructured : np.ndarray
          single unstructured light pattern
        """
        width, height = dsize
        
        # To avoid periodicity, generates pattern 
        # larger than the desired width (say 110% larger)
        scale = 1.1
        width_l = int(width * scale)
        height_l = int(height * scale)
        
        # Limit the amplitude spectrum to a single octave, 
        # ranging from frequency f to 2f 
        img_frequency = np.fromfunction(lambda y, x: np.sqrt((x-width_l/2)**2 + (y-height_l/2)**2), (height_l, width_l))
        img_mask = np.bitwise_and(f<=img_frequency, img_frequency<=2*f)
        
        # Generate white noise patterns
        n = np.count_nonzero(img_mask)
        amplitude = np.random.normal(0, 1, n)
        angle = np.random.normal(0, 1, n) * 2 * np.pi
        rnd = amplitude * np.exp(1j*angle)
        img_complex = np.zeros_like(img_mask, dtype=np.complex128)
        img_complex[img_mask] = rnd
        
        # Take the inverse 2D Fourier transform, 
        # giving a periodic pattern image
        img_complex_shift = np.fft.ifftshift(img_complex)
        img_periodic_pattern_l = np.fft.ifft2(img_complex_shift).real
        
        # Cut the extra borders
        y = (height_l - height) // 2
        x = (width_l - width) // 2
        img_periodic_pattern = img_periodic_pattern_l[y:y+height, x:x+width]

        # The pattern intensities are then rescaled 
        # to have values ranging in [0:1]
        i_min = np.min(img_periodic_pattern)
        i_max = np.max(img_periodic_pattern)
        if (i_max - i_min) != 0:
            img_periodic_pattern_rescaled = (img_periodic_pattern - i_min) / (i_max - i_min)
        else:
            img_periodic_pattern_rescaled = img_periodic_pattern
        
        # Each pattern is finally binarized 
        # by the use of a threshold at intensity 0.5 to make pixels either black (<=0.5) or white (>0.5).
        img_unstructured = np.zeros((height, width), dtype=np.uint8)
        img_unstructured[img_periodic_pattern_rescaled > 0.5] = 255

        return img_unstructured
