"""
Capture projection pattern and decode both xy.
"""
import cv2
import numpy as np
import structuredlight as sl

def imshowAndCapture(cap, img_pattern, delay=250):
    cv2.imshow("", img_pattern)
    cv2.waitKey(delay)
    ret, img_frame = cap.read()
    img_gray = cv2.cvtColor(img_frame, cv2.COLOR_BGR2GRAY)
    return img_gray

def main():
    width  = 640
    height = 480

    cap = cv2.VideoCapture(1) # External web camera
    gray = sl.Gray()
   
    
    # Generate and Decode x-coord
    # Generate
    imlist_posi_x_pat = gray.generate((width, height))
    imlist_nega_x_pat = sl.invert(imlist_posi_x_pat)

    # Capture
    imlist_posi_x_cap = [ imshowAndCapture(cap, img) for img in imlist_posi_x_pat]
    imlist_nega_x_cap = [ imshowAndCapture(cap, img) for img in imlist_nega_x_pat]
    
    # Decode
    img_index_x = gray.decode(imlist_posi_x_cap, imlist_nega_x_cap)

    
    # Generate and Decode y-coord
    # Generate
    imlist = gray.generate((height, width))
    imlist_posi_y_pat = sl.transpose(imlist)
    imlist_nega_y_pat = sl.invert(imlist_posi_y_pat)
    
    # Capture
    imlist_posi_y_cap = [ imshowAndCapture(cap, img) for img in imlist_posi_y_pat]
    imlist_nega_y_cap = [ imshowAndCapture(cap, img) for img in imlist_nega_y_pat]
    
    # Decode
    img_index_y = gray.decode(imlist_posi_y_cap, imlist_nega_y_cap)
   

    # Visualize decode result
    img_correspondence = cv2.merge([0.0*np.zeros_like(img_index_x), img_index_x/width, img_index_y/height])
    img_correspondence = np.clip(img_correspondence*255.0, 0, 255).astype(np.uint8)
    cv2.imshow("x:Green, y:Red", img_correspondence)
    cv2.waitKey(0)
    cv2.imwrite("correspondence.png", img_correspondence)
    cv2.destroyAllWindows()
    cap.release()

if __name__=="__main__":
    main()
