"""
Export all structured light patterns
"""
import os
import cv2
import structuredlight as sl

def main():
    width = 320
    height = 240
    # Structued Light instance list
    slins_list  = [sl.Binary(), sl.Gray(), sl.XOR(), sl.Ramp(), sl.PhaseShifting(), sl.Stripe()]
    # Structure Light name list
    slname_list = ["binary", "gray", "xor", "ramp", "phaseshifting", "stripe"]

    for slins, slname in zip(slins_list, slname_list):
        imlist = slins.generate((width, height))
        
        # Make directory if it doesn't exist
        dirname = slname + "{0}x{1}".format(width, height)
        if os.path.isdir(dirname) == False:
            os.makedirs(dirname)
        
        # Export images
        zero_pad = len(str(len(imlist)))
        for i, img in enumerate(imlist):
            filename = slname + str(i+1).zfill(zero_pad) + ".png"
            cv2.imwrite(dirname+"/"+filename, img)

if __name__=="__main__":
    main()
