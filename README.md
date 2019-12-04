# structured_light

## Usage
### Export images
The following example exports 256x180 gray code pattern images.
```
$ python3 gray.py 256 180
Export gray code images
./posi-1.png
./posi-2.png
./posi-3.png
./posi-4.png
./posi-5.png
./posi-6.png
./posi-7.png
./posi-8.png
./nega-1.png
./nega-2.png
./nega-3.png
./nega-4.png
./nega-5.png
./nega-6.png
./nega-7.png
./nega-8.png
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
