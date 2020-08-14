import numpy as np
from structuredlight import StructuredLight

"""
Checker is not structured-light.
It separate the direct and global components.

For more detail, read Nayar's paper below.
S.K. Nayar, G. Krishnan, M. D. Grossberg, R. Raskar, "Fast Separation of Direct and Global Components of a Scene using High Frequency Illumination", ACM Trans. on Graphics, Jul. 2006.
"""

class Checker(StructuredLight):
    def __init__(self, sqsize=3, step=1):
        self.sqsize = sqsize
        self.step = step

    def generate(self, dsize):
        width, height = dsize
        num_x = num_y = self.sqsize//self.step

        #generate
        imgs4D_code = 255*np.fromfunction(lambda y,x,ny,nx: (((x+nx*self.step)//self.sqsize)+((y+ny*self.step)//self.sqsize))%2, (height,width,num_y,num_x), dtype=int).astype(np.uint8)
        imgs_code = np.reshape(imgs4D_code, (height, width, num_y*num_x))
        
        imlist = self.split(imgs_code)
        return imlist

    def decode(self, imlist):
        imgs_code = self.merge(imlist)
        dtype = imgs_code.dtype

        img_max = np.max(imgs_code, axis=2)
        img_min = np.min(imgs_code, axis=2)
        
        max_val = np.iinfo(dtype).max if (dtype==np.uint8 or dtype==np.uint16) else np.finfo(dtype).max
        img_direct = np.clip(img_max - img_min, 0, max_val).astype(dtype)
        img_global = np.clip(    2.0 * img_min, 0, max_val).astype(dtype)
        return img_direct, img_global
