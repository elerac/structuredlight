import cv2
import numpy as np

def int2bin(n):
    if n:
        bits = []
        while n:
            n,remainder = divmod(n, 2)
            bits.insert(0, remainder)
        return bits
    else:
         return [0]
 
def bin2gray(bits):
    return bits[:1] + [i ^ ishift for i, ishift in zip(bits[:-1], bits[1:])]

def zero_padding(code, length):
    pad = length - len(code)
    if pad == 0:
        return code
    bits = [0] * pad
    bits.extend(code)
    return bits

def generate(width, height, stripe_type=0, inverse=False):
    #0:vertical stripes, 1:horizontal stripes
    if stripe_type==0:
        w = height
        h = width
    elif stripe_type==1:
        w = width
        h = height

    maxlen = len(int2bin(h))
    bits = []
    for i in range(h):
        bits.append(zero_padding(bin2gray(int2bin(i)), maxlen))
    line = np.zeros((h), np.uint8)
    img_list = []
    for i in range(maxlen):
        for j in range(h):
            line[j] = bits[j][i]*255
        img = line
        for k in range(w-1):
            img = cv2.hconcat([img, line])

        if inverse==True:
            img = 255 - img

        if stripe_type==0:
            img_list.append(img.T)
        elif stripe_type==1:
            img_list.append(img)
        
    return img_list

def decode(posi_list, nega_list):
    N = len(posi_list)

    shape = posi_list[0].shape

    c = len(shape)
    h, w = shape[:2]
    img_decode = np.zeros((h, w))
    for i in range(N):
        #binarize
        diff = -nega_list[i].astype(np.float64)+posi_list[i].astype(np.float64)
        img_bin = (diff >= 0)*255

        if c==3:
            img_bin = cv2.split(img_bin)[0]
        
        #Decode
        if i==0:
            binary = img_bin.copy()
        else:
            binary = cv2.bitwise_xor(binary, img_bin)
        img_decode += (binary/255)*(2**(N-i-1))
    
    return img_decode.astype(np.uint16)
