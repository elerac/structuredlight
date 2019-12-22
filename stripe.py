import numpy as np

def generate(width, height, stripe_type=0):
    #0:vertical stripes, 1:horizontal stripes
    if stripe_type==0:
        depth = width
        stripe_pattern = np.fromfunction(lambda y,x,d: x==d, (height, width, depth), dtype=int).astype(np.uint8)
    else:
        depth = height
        stripe_pattern = np.fromfunction(lambda y,x,d: y==d, (height, width, depth), dtype=int).astype(np.uint8)

    stripe_pattern *= 255
    imgs_stripe = list(stripe_pattern.transpose(2, 0, 1))
    return imgs_stripe

def decode(imgs_cap):
    index_decode = np.argmax(np.array(imgs_cap), axis=0)
    return index_decode

def main():
    import cv2
    import os
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("width", type=int, help="width")
    parser.add_argument("height", type=int, help="height")
    parser.add_argument("-t", "--type", type=int, default=0, help="stripe type (0:vertical, Others:horizontal)")
    parser.add_argument("-o", "--out", type=str, default=".", help="output directory")
    args = parser.parse_args()
    
    width = args.width
    height = args.height
    stripe_type = args.type

    #generate stripe images
    imgs_stripe = generate(width, height, stripe_type=stripe_type)

    #decode stripe images
    #img_decode = decode(imgs_stripe)

    #export stripe images
    out_dir = args.out
    if os.path.isdir(out_dir)==False:
        ret = os.makedirs(out_dir)
        if ret==False:
            print("false mkdir")
            return -1
        else:
            print("mkdir {}".format(out_dir))
   
    print("Export stripe images")
    for i, img in enumerate(imgs_stripe):
        name = os.path.join(out_dir, "stripe-{0}.png".format(i+1))
        print(name)
        cv2.imwrite(name, img)

if __name__=="__main__":
    main()
