#############
# imports
#############

import cv2
import pygame

from HandDetector import HandDetector

#########
# main function
#########
def main():
    # make a hand detector
    handDetector = HandDetector()

    # while the opencv window is running
    while handDetector.shouldClose == False:
        # update the webcam feed and hand tracker calculations
        handDetector.update()

        # if there is at least one hand seen, then
        # print out the landmark positions
        if len(handDetector.landmarkDictionary) > 0: 
            print(handDetector.landmarkDictionary[0])

    # Closes all the frames
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()



