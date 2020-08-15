"""
Measuring MTF (Modulation Transfer Function) simulation using PhaseShifting
"""
import numpy as np
import cv2
import matplotlib.pyplot as plt
import structuredlight as sl

def applyBlur(img_pattern):
    # Scene info
    k = 5 # Kernel size. By changing the amount of blur, the MTF changes.
    img_captured = cv2.GaussianBlur(img_pattern, ksize=(k, k), sigmaX=0)
    return img_captured

def main():
    width  = 256
    height = 256

    # Image coordinates to plot
    ix = width//2
    iy = height//2
    
    # Spatial frequency
    Fmax = 100 # Maximum freq
    Fmin = 0.1 # Minimum freq
    Nf = 50    # Number of frequency types
    frequency_list = list(np.linspace(Fmin, Fmax, num=Nf)) # All frequency

    # Phase Shifting
    ps = sl.PhaseShifting(num=10)
    
    # First, project an all-white pattern and check the maximum reflection intensity.
    img_white_pattern = np.full((height, width), 255, dtype=np.uint8)
    img_white_captured = applyBlur(img_white_pattern)
    max_intensity = 0.5*img_white_captured[iy, ix]
    
    # Next, the reflection intensity is measured while varying the frequency.
    imlist_amplitude = []
    for F in frequency_list:
        ps.F = F
        imlist_pattern = ps.generate((width, height))
        imlist_captured = [ applyBlur(img) for img in imlist_pattern]
        img_amplitude = ps.decodeAmplitude(imlist_captured)
        imlist_amplitude.append(img_amplitude)
        cv2.imshow("pattern",  imlist_pattern[0].astype(np.uint8))
        cv2.imshow("captured", imlist_captured[0].astype(np.uint8))
        cv2.waitKey(100)

    imgs_amplitude = cv2.merge(imlist_amplitude)
    imgs_ratio = imgs_amplitude/max_intensity
    
    # Plot
    ratio = imgs_ratio[iy, ix]
    plt.plot(frequency_list, ratio)
    plt.xlabel("Frequency")
    plt.ylabel("Intensity")
    plt.xlim(0, Fmax)
    plt.ylim(0.0, 1.0)
    plt.show()

if __name__=="__main__":
    main()
