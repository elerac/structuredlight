import numpy as np

class StructuredLight:
    def generate(self, dsize):
        # dsize = (width, height)
        raise NotImplementedError()

    def decode(self):
        raise NotImplementedError()
    
    @staticmethod
    def split(mv):
        return list(mv.transpose(2, 0, 1))

    @staticmethod
    def merge(m):
        return np.dstack(m)
    
    @staticmethod
    def binarize(src, thresh):
        """
        Binaryization
        Depending on the combination of the argument types, it is possible to change the method of binaryization.
        * Simple thresholding    -> (src:1, thresh:0) or (src:2, thresh:0) or (src:3, thresh:0)
        * Per-pixel thresholding -> (src:1, thresh:1) or (src:2, thresh:1) or (src:3, thresh:1)
        * Posi-Nega comparing    -> (src:2, thresh:2) or (src:3, thresh:3)
        
        src : ndarray
            1. array (height, width)
            2. array (height, width, num)
            3. list of array:1, length is num
        thresh : array or single digit(int or float)
            0. digit
            1. array (height, width)
            2. array (height, width, num)
            3. list of array:1, length is num
        """
        if type(src)    == list:
            src    = np.dstack(src)    # (src:3, *) case
        if type(thresh) == list:
            thresh = np.dstack(thresh) # (*, thresh:3) case
        
        if type(thresh) == np.ndarray:
            if src.ndim == 3 and thresh.ndim == 2: # (src:2, thresh:1) case
                thresh = np.dstack([thresh]*src.shape[2])
        
        img_thresh = thresh * np.ones_like(src)
        img_bin = np.empty_like(src, dtype=np.uint8)
        img_bin[src>=img_thresh] = True
        img_bin[src<img_thresh] = False
        return img_bin
