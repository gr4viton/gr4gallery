import numpy as np
import cv2
# from cv2 import xfeatures2d
# import common
# from plane_tracker import PlaneTracker

from collections import Counter


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def loopCV(cap):
    print "loopCV started"

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    ims = []

    cv2.namedWindow('image')

    tbValue = 3
    maxValue = 6
    cv2.createTrackbar("trackMe", "image", tbValue, maxValue, update)
    loopCV(cap)
    cap.release()
    cv2.destroyAllWindows()
