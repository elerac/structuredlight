import numpy as np
from typing import List, Tuple

class Zncc:
    """ZNCC based decoder

    ZNCC(Zero-mean Normalized Cross Correlation) based decoder can decode *arbitrary* structured light.
    
    Mirdehghan et al. show that the ZNCC-based decoder has 
    almost the same performance as the native decoder [1] (see Figure 5).
    
    References
    ----------
    .. [1] Mirdehghan et al., "Optimal structured light a la carte." CVPR 2018.
    """

    def decode(self, imlist_code: List[np.ndarray], imlist_observe: List[np.ndarray]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Parameters
        ----------
        imlist_code : List[np.ndarray]
          The projected patterns
        imlist_observe : List[np.ndarray]
          The images captured by the camera
        
        Returns
        -------
        img_index_x : np.ndarray
          index x-axis
        img_index_y : np.ndarray
          index y-axis
        """
        num = len(imlist_code)
        code = np.reshape(imlist_code, (num, -1))
        observe = np.reshape(imlist_observe, (num, -1))
        
        # Calculate ZNCC
        zncc = self.calculate_zncc(code, observe)
        
        # Get argmax
        ids = np.argmax(zncc, axis=0)

        index_y, index_x = np.unravel_index(ids, imlist_code[0].shape)
        
        dsize_observe = imlist_observe[0].shape
        img_index_y = np.reshape(index_y, dsize_observe)
        img_index_x = np.reshape(index_x, dsize_observe)

        return img_index_x, img_index_y

    @staticmethod
    def calculate_zncc(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """Calculate ZNCC (Zero-mean Normalized Cross-Correlation) for 1D or 2D array.

        Parameters
        ----------
        a : np.ndarray
           1D or 2D array. Shape should be ('N', 'any1').
        b : np.ndarray
           1D or 2D array. Shape should be ('N', 'any2').
        
        Returns
        -------
        output : np.ndarray
          Scalar or 1D array or 2D array of ZNCC value. 
          Shape is ('any1', 'any2').
        
        Examples
        --------
        Simple 1D array case
        >>> a = np.random.rand(10)
        >>> calculate_zncc(a, a) # same array
        1.0
        >>> calculate_zncc(a, -a) # invert array
        -1.0
        >>> calculate_zncc(a, 0.8*a+1.0) # change amplitude and offset
        1.0
        Simple image case
        >>> img = np.random.rand(256, 256, 3) 
        >>> calculate_zncc(img.flatten(), img.flatten())
        1.0

        2D array case
        >>> b = np.random.rand(10, 100)
        >>> c = np.random.rand(10, 200)
        >>> calculate_zncc(b, c).shape
        (100, 200)
        """
        # Subtract the average
        a = a - np.average(a, axis=0)
        b = b - np.average(b, axis=0)
        
        # Calculate the ZNCC
        aa_sum = np.expand_dims(np.sum(a*a, axis=0), -1)
        bb_sum = np.expand_dims(np.sum(b*b, axis=0), -1)
        output = ( a.T @ b ) / np.sqrt( aa_sum @ bb_sum.T )

        return output
