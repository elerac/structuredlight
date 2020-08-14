import numpy as np
from structuredlight import StructuredLight

class Binary(StructuredLight):
    def generate(self, dsize):
        width, height = dsize
        num = len(bin(width-1))-2

        imgs_code = 255*np.fromfunction(lambda y,x,n: (x&(1<<(num-1-n))!=0), (height,width,num), dtype=int).astype(np.uint8)
        
        imlist = self.split(imgs_code)
        return imlist

    def decode(self, imlist, thresh):
        height, width = imlist[0].shape[:2]
        num = len(imlist)

        # Binaryization
        imgs_code = self.binarize(imlist, thresh)

        # Decode
        cofficient = np.fromfunction(lambda y,x,n: 2**(num-1-n), (height,width,num), dtype=int)
        img_index = np.sum(imgs_code * cofficient, axis=2)
        return img_index
