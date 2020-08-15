import numpy as np
from structuredlight import StructuredLight

class Ramp(StructuredLight):
    def __init__(self):
        self.width = None

    def generate(self, dsize):
        width, height = dsize
        self.width = width

        img_white = 255*np.ones((height, width), dtype=np.uint8)
        img_ramp  = (255*np.fromfunction(lambda y,x: x/(width-1), (height,width), dtype=float)).astype(np.uint8)
        
        imlist = [img_white, img_ramp]
        return imlist

    def decode(self, imlist):
        img_ratio = self.decodeRatio(imlist)
        img_index = img_ratio*(self.width-1)
        return img_index

    def decodeRatio(self, imlist):
        img_white = imlist[0]
        img_ramp  = imlist[1]
        img_ratio = img_ramp/img_white
        return img_ratio
