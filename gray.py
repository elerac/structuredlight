import numpy as np

def generate(width, height, stripe_type=0, inverse=False):
    #0:vertical stripes, 1:horizontal stripes
    if stripe_type!=0:
        height, width = width, height
    
    depth = len(bin(width-1))-2

    #generate
    gray_pattern = np.flip(np.fromfunction(lambda y,x,d: ((x^(x>>1))&(1<<d)!=0), (height,width,depth), dtype=int).astype(np.uint8), axis=2)
    
    if stripe_type!=0:
        gray_pattern = gray_pattern.transpose(1, 0, 2)

    if inverse==True:
        gray_pattern = True - gray_pattern
    
    gray_pattern *= 255
    imgs_gray = list(gray_pattern.transpose(2, 0, 1))
    return imgs_gray

def decode(imgs_posi, imgs_nega):
    height, width = imgs_posi[0].shape[:2]
    depth = len(imgs_posi)

    #binarization
    posi = np.array(imgs_posi).transpose(1, 2, 0)
    nega = np.array(imgs_nega).transpose(1, 2, 0)
    gray_pattern = np.empty((height, width, depth), dtype=np.uint8)
    gray_pattern[posi>=nega] = True
    gray_pattern[posi<nega] = False

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
    parser.add_argument("-t", "--type", type=int, default=0, help="stripe type (0:vertical, Other:horizontal)")
    parser.add_argument("-o", "--out", type=str, default=".", help="output directory")
    args = parser.parse_args()
    
    width = args.width
    height = args.height
    stripe_type = args.type

    #generate gray code images
    imgs_posi = generate(width, height, stripe_type=stripe_type, inverse=False)
    imgs_nega = generate(width, height, stripe_type=stripe_type, inverse=True)

    #decode gray code images
    img_decode = decode(imgs_posi, imgs_nega)

    #export gray code images
    out_dir = args.out
    if os.path.isdir(out_dir)==False:
        ret = os.makedirs(out_dir)
        if ret==False:
            print("false mkdir")
            return -1
        else:
            print("mkdir {}".format(out_dir))
   
    print("Export gray code images")
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
