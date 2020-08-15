import numpy as np

def transpose(imlist):
    """
    Replacing the x-axis and y-axis of an image in the list of images
    """
    return [ img.T for img in imlist]

def invert(imlist):
    """
    Invert the color of an image in the list of images
    """
    return [ 255-img for img in imlist]
