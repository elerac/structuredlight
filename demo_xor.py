import cv2
import numpy as np
import xor

def main():
    #出力するプロジェクターの解像度
    size = (720, 1280)
    h, w = size
    
    index_last = -1
    stripe_type = 0 #0:vertical stripes, 1:horizontal stripes
    imgs_posi = xor.generate(w, h, index_last, stripe_type, inverse=False)
    imgs_nega = xor.generate(w, h, index_last, stripe_type, inverse=True)

    for img in imgs_posi:
        cv2.imshow("image", img)
        cv2.waitKey(100)
    
    for img in imgs_nega:
        cv2.imshow("image", img)
        cv2.waitKey(100)

    img_decode = xor.decode(imgs_posi, imgs_nega, index_last)
    
    MAX = 2**len(imgs_posi)-1
    img_dst = (np.clip((img_decode/MAX*65535), 0, 65535)).astype(np.uint16)

    cv2.imshow("image", img_dst)
    cv2.waitKey(0)

    cv2.destroyAllWindows()

if __name__=='__main__':
    main()
