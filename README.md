# structured_light
These programs generate and decode structured light. Currently supports Binary code, Gray code, XOR code, Unstructured light and Single stripe.

## Usage
### Export images
The following example exports 256x180 gray code pattern images.
```
$ python3 gray.py 256 180
```

### Use as a module
```python
import gray

width = 1280
height = 800

imgs_posi = gray.generate(width, height, inverse=False)
imgs_nega = gray.generate(width, height, inverse=True)

#Projecting patterns from a projector
#Capture images

decode = gray.decode(imgs_posi, imgs_nega)
print(decode)
```
