import numpy as np
from typing import Tuple

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

def getCorrespondencePoints(img_correspondence_x: np.ndarray, 
                           img_correspondence_y: np.ndarray=None, 
                           img_mask: np.ndarray=None) -> Tuple[np.ndarray]:
    """
    Convert a correspondence points from the correspondence map image

    ```
    # Usage
    import structuredlight as sl
    gray = sl.Gray()
    imlist = gray.generate((640, 480))
    img_index_x = gray.decode(imlist)
    campoints, prjpoints = sl.getCorrespondenceTable(img_index_x)
    ```

    Parameters
    ----------
    img_correspondence_x : np.ndarray, (height, width)
        x-coorde correspondence map image
    img_correspondence_y : np.ndarray, (height, width)
        y-coorde correspondence map image (option)
    img_mask : np.ndarray, (height, width)
        mask image (option)

    Returns
    -------
    campoints : np.ndarray, (N, 2)
        2D camera points
        [[x1, y1], [x2, y2], ..., [xn,yn]]
    prjpoints : np.ndarray, (N,) or (N, 2)
        2D camera points
        [[x1, x2, ...,xn]
        or
        [[x1, y1], [x2, y2], ..., [xn,yn]]
    """
    # Camera points
    height_cam, width_cam = img_correspondence_x.shape[:2]
    if img_mask is None:
        img_mask = np.ones((height_cam, width_cam))
    cam_y, cam_x = np.where(np.ones((height_cam, width_cam)) * img_mask)
    campoints = np.array([cam_x, cam_y]).T
    
    # Projector points
    if img_correspondence_y is None:
        prj_x = img_correspondence_x[cam_y, cam_x]
        prjpoints = prj_x
    else:
        prj_x = img_correspondence_x[cam_y, cam_x]
        prj_y = img_correspondence_y[cam_y, cam_x]
        prjpoints = np.array([prj_x, prj_y]).T
    
    return campoints, prjpoints
