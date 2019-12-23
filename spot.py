import numpy as np

def generate(width, height):
    spot_pattern = np.fromfunction(lambda y,x,dh,dw: (x==dw)*(y==dh), (height, width, height, width), dtype=int).astype(np.uint8)

    spot_pattern = np.reshape(spot_pattern, (height, width, height*width))

    spot_pattern *= 255
    imgs_spot = list(spot_pattern.transpose(2, 0, 1))
    return imgs_spot

def decode(imgs_cap, width_proj, height_proj):
    index_decode = np.array(np.unravel_index(np.argmax(np.array(imgs_cap), axis=0), (height_proj, width_proj))).transpose(1, 2, 0)
    return list(index_decode.transpose(2, 0, 1))

def main():
    import cv2
    import os
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("width", type=int, help="width")
    parser.add_argument("height", type=int, help="height")
    parser.add_argument("-o", "--out", type=str, default=".", help="output directory")
    args = parser.parse_args()
    
    width = args.width
    height = args.height

    #generate spot images
    imgs_spot = generate(width, height)

    #decode spot images
    #decode_h, decode_v = decode(imgs_spot, width, height)

    #export spot images
    out_dir = args.out
    if os.path.isdir(out_dir)==False:
        ret = os.makedirs(out_dir)
        if ret==False:
            print("false mkdir")
            return -1
        else:
            print("mkdir {}".format(out_dir))
   
    print("Export spot images")
    for i, img in enumerate(imgs_spot):
        name = os.path.join(out_dir, "spot-{0}.png".format(i+1))
        print(name)
        cv2.imwrite(name, img)

if __name__=="__main__":
    main()
