"""
Export decode result (camera-projector correspondence index) as csv format
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
    corr_table = sl.getCorrespondenceTable(img_index_x)
    np.savetxt("correspondence_x.csv", corr_table, delimiter=",")
    print("[cam_x cam_y prj_x]")
    print(corr_table)
    
    # both xy-coord
    corr_table = sl.getCorrespondenceTable(img_index_x, img_index_y)
    np.savetxt("correspondence_xy.csv", corr_table, delimiter=",")
    print("[cam_x cam_y prj_x prj_y]")
    print(corr_table)
    
if __name__=="__main__":
    main()
