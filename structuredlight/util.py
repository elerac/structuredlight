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

def getCorrespondenceTable(img_index_x, img_index_y=None):
    """
    Convert a correspondence table from the index image.

    correspondence_table : array_like
        correspondence table of camera index and projector index
        array shape is (height_cam*width_cam, 3 or 4)
        cam_x, cam_y, proj_x, proj_y (or not)
    """
    height_cam, width_cam = img_index_x.shape[:2]
    cam_y, cam_x = np.where(np.ones((height_cam, width_cam))) # camera image index x, y
    
    prj_x = img_index_x[cam_y, cam_x]
    
    if img_index_y is not None:
        prj_y = img_index_y[cam_y, cam_x]
        correspondence_table = np.stack([cam_x, cam_y, prj_x, prj_y]).astype(np.uint16).T
    else:
        correspondence_table = np.stack([cam_x, cam_y, prj_x]).astype(np.uint16).T
    
    return correspondence_table
