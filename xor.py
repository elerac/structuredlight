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

def generate(width, height, index_last=-1, stripe_type=0, inverse=False):
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

        if stripe_type==0:
            img_list.append(img.T)
        elif stripe_type==1:
            img_list.append(img)

    #gray to xor
    last_pattern = img_list[index_last].copy()
    for i, img in enumerate(img_list):
        img_list[i] = cv2.bitwise_xor(img, last_pattern)
    img_list[index_last] = last_pattern.copy()
        
    if inverse==True:
        img_list = [255-img for img in img_list]
        
    return img_list

def decode(posi_list, nega_list, index_last=-1):
    N = len(posi_list)

    shape = posi_list[0].shape
        
    diff = -nega_list[index_last].astype(np.float64)+posi_list[index_last].astype(np.float64)
    last_pattern = np.zeros(shape, dtype=np.uint8)
    last_pattern[diff>=0] = 255
    last_pattern[diff<0] = 0

    img_decode = np.zeros(shape)
    img_list = []
    for i in range(N):
        #binarize
        diff = -nega_list[i].astype(np.float64)+posi_list[i].astype(np.float64)
        img_bin = np.zeros(shape, dtype=np.uint8)
        img_bin[diff>=0] = 255
        img_bin[diff<0] = 0
        
        #xor to gray
        img_bin = cv2.bitwise_xor(img_bin, last_pattern)
        img_list.append(img_bin)
    img_list[index_last] = last_pattern
        
    for i, img_bin in enumerate(img_list):
        #Decode
        if i==0:
            binary = img_bin.copy()
        else:
            binary = cv2.bitwise_xor(binary, img_bin)
        img_decode += (binary/255)*(2**(N-i-1))
    
    return img_decode.astype(np.uint16)
