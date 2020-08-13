import numpy as np
from structuredlight import StructuredLight

class XOR(StructuredLight):
    def __init__(self, index_last=-1):
        self._index_last = index_last

    def generate(self, dsize):
        width, height = dsize
        num = len(bin(width-1))-2

        img_gray = 255*np.fromfunction(lambda y,x,n: ((x^(x>>1))&(1<<(num-1-n))!=0), (height,width,num), dtype=int).astype(np.uint8)
        
        # Convert gray code to xor code
        img_xor = np.empty((height, width, num), dtype=np.uint8)
        img_last = img_gray[:,:,self._index_last].copy()
        for i in range(num):
            img_xor[:,:,i] = np.bitwise_xor(img_gray[:,:,i], img_last)
        img_xor[:,:,self._index_last] = img_last.copy()
        
        patternImages = self.split(img_xor)
        return patternImages

    def decode(self, patternImages, thresh):
        height, width = patternImages[0].shape[:2]
        num = len(patternImages)

        # Binaryization
        img_xor = self.binarize(patternImages, thresh)

        # Convert xor code to gray code
        img_last = img_xor[:,:,self._index_last]
        img_gray = np.empty((height, width, num), dtype=np.uint8)
        for i in range(num):
            img_gray[:,:,i] = np.bitwise_xor(img_xor[:,:,i], img_last)
        img_gray[:,:,self._index_last] = img_last.copy()

        # Convert gray code to binary code
        img_binary = img_gray
        for i in range(1, num):
            img_binary[:,:,i] = np.bitwise_xor(img_binary[:,:,i], img_binary[:,:,i-1])

        # Decode
        cofficient = np.fromfunction(lambda y,x,n: 2**(num-1-n), (height,width,num), dtype=int)
        img_index = np.sum(img_binary * cofficient, axis=2)
        return img_index
