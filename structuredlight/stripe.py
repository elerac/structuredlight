import numpy as np
from structuredlight import StructuredLight

class Stripe(StructuredLight):
    def generate(self, dsize):
        width, height = dsize
        num = width

        img_code = 255*np.fromfunction(lambda y,x,n: x==n, (height, width, num), dtype=int).astype(np.uint8)
        
        patternImages = self.split(img_code)
        return patternImages

    def decode(self, patternImages):
        index_decode = np.argmax(patternImages, axis=0)
        return index_decode
