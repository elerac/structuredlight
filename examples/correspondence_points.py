"""
Convert decode result to correspondence points
"""
import cv2
import numpy as np
import structuredlight as sl

def main():
    width  = 320
    height = 240

    gray = sl.Gray()
  
    # x-coord
    imlist_pattern_x = gray.generate((width, height))
    img_index_x = gray.decode(imlist_pattern_x, thresh=127)
    
    # y-coord
    imlist_pattern_y = sl.transpose( gray.generate((height, width)) )
    img_index_y = gray.decode(imlist_pattern_y, thresh=127)

    # Export correspondence table
    # x-coord only
    campoints, prjpoints = sl.getCorrespondencePoints(img_index_x)
    print("x-coord only")
    print("campoints: ", campoints.shape)
    print(campoints)
    print("prjpoints: ", prjpoints.shape)
    print(prjpoints)
    
    # both xy-coord
    campoints, prjpoints = sl.getCorrespondencePoints(img_index_x, img_index_y)
    print("xy-coord only")
    print("campoints: ", campoints.shape)
    print(campoints)
    print("prjpoints: ", prjpoints.shape)
    print(prjpoints)
    
if __name__=="__main__":
    main()
