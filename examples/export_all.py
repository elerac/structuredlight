import os
import cv2
import structuredlight as sl

def main():
    width = 320
    height = 240
    slins_list = [sl.Binary(), sl.Gray(), sl.XOR(), sl.Ramp(), sl.PhaseShifting(), sl.Stripe()]
    slname_list = ["binary", "gray", "xor", "ramp", "phaseshifting", "stripe"]

    for slins, slname in zip(slins_list, slname_list):
        images = slins.generate((width, height))
        
        dirname = slname + "{0}x{1}".format(width, height)
        if os.path.isdir(dirname) == False:
            os.makedirs(dirname)

        zero_pad = len(str(len(images)))
        for i, img in enumerate(images):
            filename = slname + str(i+1).zfill(zero_pad) + ".png"
            cv2.imwrite(dirname+"/"+filename, img)

if __name__=="__main__":
    main()
