import numpy as np
from structuredlight import StructuredLight

class Gray(StructuredLight):
    def generate(self, dsize):
        width, height = dsize
        num = len(bin(width-1))-2

        imgs_code = 255*np.fromfunction(lambda y,x,n: ((x^(x>>1))&(1<<(num-1-n))!=0), (height,width,num), dtype=int).astype(np.uint8)
        
        imlist = self.split(imgs_code)
        return imlist

    def decode(self, imlist, thresh):
        height, width = imlist[0].shape[:2]
        num = len(imlist)

        # Binaryization
        imgs_gray = self.binarize(imlist, thresh)

        # Convert gray code to binary code
        imgs_binary = imgs_gray
        for i in range(1, num):
            imgs_binary[:,:,i] = np.bitwise_xor(imgs_binary[:,:,i], imgs_binary[:,:,i-1])

        # Decode
        cofficient = np.fromfunction(lambda y,x,n: 2**(num-1-n), (height,width,num), dtype=int)
        img_index = np.sum(imgs_binary * cofficient, axis=2)
        return img_index
