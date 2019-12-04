import numpy as np

def generate(width, height, index_last=-1, stripe_type=0, inverse=False):
    #0:vertical stripes, 1:horizontal stripes
    if stripe_type!=0:
        height, width = width, height
    
    depth = len(bin(width-1))-2

    #generate
    gray_pattern = np.flip(np.fromfunction(lambda y,x,d: ((x^(x>>1))&(1<<d)!=0), (height,width,depth), dtype=int).astype(np.uint8), axis=2)

    xor_pattern = np.empty((height, width, depth), dtype=np.uint8)
    img_last = gray_pattern[:,:,index_last].copy()
    for i in range(depth):
        xor_pattern[:,:,i] = np.bitwise_xor(gray_pattern[:,:,i], img_last)
    xor_pattern[:,:,index_last] = img_last.copy()
    
    if stripe_type!=0:
        xor_pattern = xor_pattern.transpose(1, 0, 2)

    if inverse==True:
        xor_pattern = True - xor_pattern
    
    xor_pattern *= 255
    imgs_xor = list(xor_pattern.transpose(2, 0, 1))
    return imgs_xor

def decode(imgs_posi, imgs_nega, index_last=-1):
    height, width = imgs_posi[0].shape[:2]
    depth = len(imgs_posi)

    #binarization
    posi = np.array(imgs_posi).transpose(1, 2, 0)
    nega = np.array(imgs_nega).transpose(1, 2, 0)
    xor_pattern = np.empty((height, width, depth), dtype=np.uint8)
    xor_pattern[posi>=nega] = True
    xor_pattern[posi<nega] = False
    img_last = xor_pattern[:,:,index_last]

    #xor_pattern > gray_pattern
    gray_pattern = np.empty((height, width, depth), dtype=np.uint8)
    for i in range(depth):
        gray_pattern[:,:,i] = np.bitwise_xor(xor_pattern[:,:,i], img_last)
    gray_pattern[:,:,index_last] = img_last.copy()

    #gray_pattern > binary_pattern
    binary_pattern = gray_pattern.copy()
    for i in range(1, depth):
        binary_pattern[:,:,i] = np.bitwise_xor(binary_pattern[:,:,i], binary_pattern[:,:,i-1])

    #decode
    binary_cofficient = np.flip(np.fromfunction(lambda y,x,d: 2**d, (height,width,depth), dtype=int), axis=2)
    index_decode = np.sum(binary_pattern * binary_cofficient, axis=2)    
    return index_decode

def main():
    import cv2
    import os
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("width", type=int, help="width")
    parser.add_argument("height", type=int, help="height")
    parser.add_argument("-t", "--type", type=int, default=0, help="stripe type (0:vertical, Others:horizontal)")
    parser.add_argument("-i", "--index_last", type=int, default=-1, help="last pattern index")
    parser.add_argument("-o", "--out", type=str, default=".", help="output directory")
    args = parser.parse_args()
    
    width = args.width
    height = args.height
    stripe_type = args.type
    index_last = args.index_last

    #generate xor code images
    imgs_posi = generate(width, height, index_last=index_last, stripe_type=stripe_type, inverse=False)
    imgs_nega = generate(width, height, index_last=index_last, stripe_type=stripe_type, inverse=True)

    #decode xor code images
    img_decode = decode(imgs_posi, imgs_nega, index_last=index_last)

    #export xor code images
    out_dir = args.out
    if os.path.isdir(out_dir)==False:
        ret = os.makedirs(out_dir)
        if ret==False:
            print("false mkdir")
            return -1
        else:
            print("mkdir {}".format(out_dir))
   
    print("Export xor code images")
    for i, img in enumerate(imgs_posi):
        name = os.path.join(out_dir, "posi-{0}.png".format(i+1))
        print(name)
        cv2.imwrite(name, img)
    for i, img in enumerate(imgs_nega):
        name = os.path.join(out_dir, "nega-{0}.png".format(i+1))
        print(name)
        cv2.imwrite(name, img)

if __name__=="__main__":
    main()
