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
```python
binary = sl.Binary()
imgs_code = binary.generate((width, height))
decode    = binary.decode(imgs_code, thresh=127)
```

### Gray code
![](documents/gray.gif)
```python
gray = sl.Gray()
imgs_code = gray.generate((width, height))
decode    = gray.decode(imgs_code, thresh=127)
```

### XOR code
![](documents/xor.gif)
```python
xor = sl.XOR(index_last=-1)
imgs_code = xor.generate((width, height))
decode    = xor.decode(imgs_code, thresh=127)
```

### Ramp code
![](documents/ramp.gif)
```python
ramp = sl.Ramp()
imgs_code = ramp.generate((width, height))
decode    = ramp.decode(imgs_code)
```

### Phase-Shifting
![](documents/phaseshifting.gif)
```python
phaseshifting = sl.PhaseShifting(num=3)
imgs_code = phaseshifting.generate((width, height))
decode    = phaseshifting.decode(imgs_code)
```

### Single stripe
![](documents/stripe.gif)
```python
stripe = sl.Stripe()
imgs_code = stripe.generate((width, height))
decode    = stripe.decode(imgs_code)
```