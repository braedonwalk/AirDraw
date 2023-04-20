# PEN MASTER 9000 #
# Created using help from the following people:
# Kevin Ponce: https://kevinponce.com/blog/python/send-gcode-through-serial-to-a-3d-printer-using-python/
# Github user TonyJacb: https://github.com/TonyJacb/Python-GcodeClient/blob/main/gcodeclient.py 
# Chris Whitmire: HandDectector script

import cv2

from Client import Client
from HandDetector import HandDetector

def main():
    # create a serial object using the Client class
    ser = Client("COM10", 115200)

    # create a handDectector object
    handDetector = HandDetector()  #include 1 for external camera
    xCoordList = []
    yCoordList = []
    coords = ()
    dropDownDistance = -40

    # while the opencv window is running
    while handDetector.shouldClose == False:
        # update the webcam feed and hand tracker calculations
        handDetector.update()

        # if there is at least one hand seen, then
        if len(handDetector.landmarkDictionary) > 0: 
            # get the coordinates of the tip of the pointer finger
            fingerX = handDetector.landmarkDictionary[0][8][0]  # [first hand][hand point][x coordinate]
            fingerY = handDetector.landmarkDictionary[0][8][1]  # [first hand][hand point][y coordinate]
            fingerZ = handDetector.landmarkDictionary[0][8][2]  # [first hand][hand point][z coordinate]

            # if the tip of the pointer finger is on screen 
            if((fingerX >= 0 and fingerY >= 0) and (fingerX <= handDetector.WIDTH and fingerY <= handDetector.HEIGHT)):
                # map their x and y to the size of pen plotter
                fingerX = constrain(map_range(fingerX, 0, handDetector.WIDTH, 0, 6), 0, 6)
                fingerY = constrain(map_range(fingerY, 0, handDetector.HEIGHT, 4, 0), 0, 4)
                
                coords = update_lists(xCoordList, yCoordList, fingerX, fingerY)
                print(coords)
                # print(fingerZ) 
                # print(fingerX, fingerY)
                drop_marker(ser, fingerZ, dropDownDistance)

                # send the gcode command using the function from the Client class
                # print("G0 X" + str(fingerX) + " Y" + str(fingerY))
                # ser.command("G0 X" + str(fingerX) + " Y" + str(fingerY))
                ser.command("G0 X" + str(coords[0]) + " Y" + str(coords[1]))

    # Closes all the frames
    cv2.destroyAllWindows()

def update_lists(xList, yList, fingerX, fingerY):
    xList.append(fingerX)
    yList.append(fingerY)

    if(len(xList) >= 30):
        xList.pop(0)
    if(len(yList) >= 30):
        yList.pop(0)

    avgX = average(xList)
    avgY = average(yList)

    # print(avgX)
    # print(avgY)
    return avgX, avgY

def drop_marker(ser, fingerZ, downDist):
    if(fingerZ < downDist):
        ser.command("M3 S150")
        # print("down boi")
    else:
        ser.command("M5")
        # print("uppies")

def average(lst):
    return sum(lst) / len(lst)

def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

def map_range(value, start1, stop1, start2, stop2):
   return (value - start1) / (stop1 - start1) * (stop2 - start2) + start2

if __name__ == "__main__":
    main()
