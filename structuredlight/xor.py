import numpy as np
from structuredlight import StructuredLight

class XOR(StructuredLight):
    def __init__(self, index_last=-1):
        self._index_last = index_last

    def generate(self, dsize):
        width, height = dsize
        num = len(bin(width-1))-2

        imgs_gray = 255*np.fromfunction(lambda y,x,n: ((x^(x>>1))&(1<<(num-1-n))!=0), (height,width,num), dtype=int).astype(np.uint8)
        
        # Convert gray code to xor code
        imgs_xor = np.empty((height, width, num), dtype=np.uint8)
        img_last = imgs_gray[:,:,self._index_last].copy()
        for i in range(num):
            imgs_xor[:,:,i] = np.bitwise_xor(imgs_gray[:,:,i], img_last)
        imgs_xor[:,:,self._index_last] = img_last.copy()
        
        imlist = self.split(imgs_xor)
        return imlist

    def decode(self, imlist, thresh):
        height, width = imlist[0].shape[:2]
        num = len(imlist)

        # Binaryization
        imgs_xor = self.binarize(imlist, thresh)

        # Convert xor code to gray code
        img_last = imgs_xor[:,:,self._index_last]
        imgs_gray = np.empty((height, width, num), dtype=np.uint8)
        for i in range(num):
            imgs_gray[:,:,i] = np.bitwise_xor(imgs_xor[:,:,i], img_last)
        imgs_gray[:,:,self._index_last] = img_last.copy()

        # Convert gray code to binary code
        imgs_binary = imgs_gray
        for i in range(1, num):
            imgs_binary[:,:,i] = np.bitwise_xor(imgs_binary[:,:,i], imgs_binary[:,:,i-1])

        # Decode
        cofficient = np.fromfunction(lambda y,x,n: 2**(num-1-n), (height,width,num), dtype=int)
        img_index = np.sum(imgs_binary * cofficient, axis=2)
        return img_index
