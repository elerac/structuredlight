import numpy as np
from structuredlight import StructuredLight

class Stripe(StructuredLight):
    def generate(self, dsize):
        width, height = dsize
        num = width

        imgs_code = 255*np.fromfunction(lambda y,x,n: x==n, (height, width, num), dtype=int).astype(np.uint8)
        
        imlist = self.split(imgs_code)
        return imlist

    def decode(self, imlist):
        img_index = np.argmax(imlist, axis=0)
        return img_index
