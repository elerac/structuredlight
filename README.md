# Structured Light
These programs generate and decode structured light. 

Currently supports 
* [Binary code](#Binary-code)
* [Gray code](#Gray-code)
* [XOR code](#XOR-code)
* [Ramp code](#Ramp-code)
* [Phase Shifting](#Phase-Shifting)
* [Single stripe](#Single-stripe)

## Requirement
* Numpy

## Installation
```sh
git clone https://github.com/elerac/structuredlight.git 
cd structuredlight
python setup.py install
```

## Usage
```python
import structuredlight as sl

width  = 640
height = 480

gray = sl.Gray()

imgs_code = gray.generate((width, height))

# Projecting patterns from a projector (or display) and capture images
imgs_captured = imgs_code

decode = gray.decode(imgs_captured, thresh=127)

print(decode)
# [[  0   1   2 ... 637 638 639]
#  [  0   1   2 ... 637 638 639]
#  ...
#  [  0   1   2 ... 637 638 639]]
```

## Supported structured light

### Binary code
![](documents/binary.gif)

### Gray code
![](documents/gray.gif)

### XOR code
![](documents/xor.gif)

### Ramp code
![](documents/ramp.gif)

### Phase-Shifting
![](documents/phaseshifting.gif)

### Single stripe
![](documents/stripe.gif)