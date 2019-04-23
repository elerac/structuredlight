# codepattern

## Usage
```
git clone https://github.com/elerac/codepattern.git
```


```python=
import cv2
import numpy as np
from codepattern import gray

def main():
    size = (720, 1280)
    h, w = size

    stripe_type = 0 #0:vertical stripes, 1:horizontal stripes
    imgs_posi = gray.generate(w, h, stripe_type, inverse=False)
    imgs_nega = gray.generate(w, h, stripe_type, inverse=True)

    for img in imgs_posi:
        cv2.imshow("image", img)
        cv2.waitKey(100)
    
    for img in imgs_nega:
        cv2.imshow("image", img)
        cv2.waitKey(100)

    img_decode = gray.decode(imgs_posi, imgs_nega)
    
    MAX = 2**len(imgs_posi)-1
    img_dst = (np.clip((img_decode/MAX*255), 0, 255)).astype(np.uint8)
    
    cv2.imshow("image", img_dst)
    cv2.waitKey(0)

    cv2.destroyAllWindows()

if __name__=='__main__':
    main()
```

## Reference
- [グレイコードパターン投影/Computational なんとか](http://blog.k-tanaka.me/archives/8)
