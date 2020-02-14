import numpy as np

def generate(width, height, sqsize=1, step=1):
    depth_x = depth_y = sqsize//step

    #generate
    checker_pattern = np.fromfunction(lambda y,x,dy,dx: (((x+dx*step)//sqsize)+((y+dy*step)//sqsize))%2, (height,width,depth_y,depth_x), dtype=int).astype(np.uint8)
    checker_pattern = np.reshape(checker_pattern, (height, width, depth_y*depth_x))
    
    checker_pattern *= 255
    imgs_checker = list(checker_pattern.transpose(2, 0, 1))
    return imgs_checker

def main():
    import cv2
    import os
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("width", type=int, help="width")
    parser.add_argument("height", type=int, help="height")
    parser.add_argument("--step", type=int, default=1, help="checker patterns shift step")
    parser.add_argument("--sqsize", type=int, default=1, help="checker size")
    parser.add_argument("-o", "--out", type=str, default=".", help="output directory")
    args = parser.parse_args()
    
    width = args.width
    height = args.height
    sqsize = args.sqsize
    step = args.step

    #generate checker pattern images
    imgs_checker = generate(width, height, sqsize=sqsize, step=step)

    #export checker pattern images
    out_dir = args.out
    if os.path.isdir(out_dir)==False:
        ret = os.makedirs(out_dir)
        if ret==False:
            print("false mkdir")
            return -1
        else:
            print("mkdir {}".format(out_dir))
   
    print("Export checker pattern images")
    for i, img in enumerate(imgs_checker):
        name = os.path.join(out_dir, "checker-{0}.png".format(i+1))
        print(name)
        cv2.imwrite(name, img)

if __name__=="__main__":
    main()
