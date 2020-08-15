"""
How to binarize a grayscale image
This program shows you how to use the three methods.
1. Simple thresholding
2. Per-pixel thresholding
3. Posi-Nega comparing
"""
import numpy as np
import structuredlight as sl

def main():
    width  = 640
    height = 480

    gray = sl.Gray()

    imlist_pattern = gray.generate((width, height))

    print("1. Simple thresholding")
    img_index = gray.decode(imlist_pattern, thresh=127)

    print("2. Per-pixel thresholding")
    img_white = np.full((height, width), 255, dtype=np.uint8)
    img_black = np.full((height, width),  0 , dtype=np.uint8)
    img_thresh = 0.5*img_white + 0.5*img_black
    img_index = gray.decode(imlist_pattern, thresh=img_thresh)

    print("3. Posi-Nega comparing")
    imlist_posi = imlist_pattern
    imlist_nega = sl.invert(imlist_posi)
    img_index = gray.decode(imlist_posi, imlist_nega)

if __name__=="__main__":
    main()
