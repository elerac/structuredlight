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

## Usage
```python
import structuredlight as sl

width  = 640
height = 480

gray = sl.Gray()

imgs_code = gray.generate((width, height))

# Projecting patterns from a projector (or display)
# And capture images
imgs_captured = imgs_code

decode = gray.decode(imgs_captured)
print(decode)
```

## Supported Structured-Light

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