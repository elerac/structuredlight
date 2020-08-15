import numpy as np

def transpose(imlist):
    return [ img.T for img in imlist]

def invert(imlist):
    return [ 255-img for img in imlist]
