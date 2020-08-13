import numpy as np
from structuredlight import StructuredLight

class PhaseShifting(StructuredLight):
    def __init__(self, num=3):
        self.num = num
    
    def generate(self, dsize):
        width, height = dsize
        num = self.num
        w = 2*np.pi/width

        img_code = (255*np.fromfunction(lambda y,x,n: 0.5*(np.cos(w*x + 2*np.pi*n/num) + 1), (height,width,num), dtype=float)).astype(np.uint8)
        
        patternImages = self.split(img_code)
        return patternImages

    def decode(self, patternImages):
        num = len(patternImages)
        
        n = np.arange(0, num)
        R = self.merge(patternImages)
        M = np.array([np.ones_like(n), np.cos(2*np.pi*n/num), -np.sin(2*np.pi*n/num)]).T #(num, 3)
        M_pinv = np.linalg.inv(M.T @ M) @ M.T #(3, num)
        U = np.tensordot(M_pinv, R, axes=(1,2)).transpose(1, 2, 0) #(height, width, 3)
        
        U1, U2, U3 = self.split(U)
        A = np.sqrt(U2**2 + U3**2)
        img_phase = np.arccos(U2/A)
        img_phase[U3<0] = 2*np.pi - img_phase[U3<0]
        
        return img_phase
