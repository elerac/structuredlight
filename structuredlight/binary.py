import numpy as np
from structuredlight import StructuredLight

class Binary(StructuredLight):
    def generate(self, dsize):
        width, height = dsize
        num = len(bin(width-1))-2

        img_code = 255*np.fromfunction(lambda y,x,n: (x&(1<<(num-1-n))!=0), (height,width,num), dtype=int).astype(np.uint8)
        
        patternImages = self.split(img_code)
        return patternImages

    def decode(self, patternImages, thresh):
        height, width = patternImages[0].shape[:2]
        num = len(patternImages)

        # Binaryization
        img_code = self.binarize(patternImages, thresh)

        # Decode
        cofficient = np.fromfunction(lambda y,x,n: 2**(num-1-n), (height,width,num), dtype=int)
        img_index = np.sum(img_code * cofficient, axis=2)
        return img_index
