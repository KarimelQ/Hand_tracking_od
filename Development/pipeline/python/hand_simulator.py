#################################################################################
#
#   25-09-2022
#   KELQ
#
#################################################################################

import cv2
import time
import numpy as np
import mediapipe as mp
import os
import shutil
from shutil import copy2

class handSimulator():
    def __init__(self, activate=True) -> None:
        """
        function :
        input :
        output :
        """
        if(activate):
            self.camera = cv2.VideoCapture(0)
            self.HandDetector = handDetector()
            self.camera_activated = True

    def take_picture(self):
        """
        function :
        input :
        output :
        """
        if(self.camera_activated == False):
            raise TypeError(" Camera desactivated, please activate")

        success, image = self.camera.read()
        if(success == False):
            raise TypeError(" error while taking picture !")

        return image

    def hand_in_image(self, handlist):
        return 1 if (len(handlist)>0) else 0

    def extract_position(self, image, index=9):
        hand_image      = self.HandDetector.findHands(image)
        handposition   = self.HandDetector.findPosition(hand_image)
        if(self.hand_in_image(handposition)):
            x = 640-np.array(handposition)[index,:][1]
            y = np.array(handposition)[index,:][2]
            # print(f'x: {x}, y:{y}')
            return x,y
        else:
            return 0,0

    def take_new_position(self):
        image = self.take_picture()
        return self.extract_position(image)

    def camera_deac(self, enable=True):
        """
        function
        input :
        output :

        """
        if(enable == True):
            self.camera = cv2.VideoCapture(0)
            self.camera_activated = True
        else:
            self.camera.release()
            self.camera_activated = False

    def images_to_video(images, video_number, video_name):
        """
        function 
        input :
        output :
        """
        out = cv2.VideoWriter(
            f'{video_name}.avi', cv2.VideoWriter_fourcc(*'DIVX'), 10, (640, 480)
        )
        for i in range(len(images)):
            out.write(images[i])
        out.release()

        destination_path = f'{os.getcwd()}/opencv/video_{video_number}'
        source_path = f'{os.getcwd()}/{video_name}.avi'
        mode = 0o777
        try:
            os.makedirs(destination_path, mode = mode, exist_ok = True)
        except OSError as error:
            print("Error while creating folder")

        shutil.move(
            source_path,
            f'{destination_path}/{video_name}.avi',
            copy_function=copy2,
        )



class handDetector():
    def __init__(self, mode = False, maxHands = 2, detectionCon = 1, trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self,img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo = 0, draw = True):
        """
        The function `findPosition` takes an image and returns a list of landmarks (id, x, y) for a
        specified hand, and optionally draws circles on the image at the landmark positions.
        Positions are in range(640,480)
        
        :param img: The "img" parameter is the image on which you want to find the hand landmarks. It should
        be a numpy array representing the image
        :param handNo: The `handNo` parameter is used to specify which hand to track. By default, it is set
        to 0, which means it will track the first hand detected. If there are multiple hands in the image,
        you can change the value of `handNo` to track a different hand, defaults to 0 (optional)
        :param draw: The "draw" parameter is a boolean value that determines whether or not to draw circles
        on the image to represent the detected landmarks. If set to True, circles will be drawn on the
        image. If set to False, no circles will be drawn, defaults to True (optional)
        :return: a list of landmarks for a specific hand in an image. Each landmark consists of an id,
        x-coordinate, and y-coordinate.
        """

        lmlist = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 3, (255, 0, 255), cv2.FILLED)
        return lmlist

    def boundingBox(self, image, handNo=0, draw=False):
        lmlist = self.findPosition(image, handNo=handNo, draw=False)
        if len(lmlist) > 0:
            x_min, y_min = lmlist[0][1], lmlist[0][2]
            x_max, y_max = lmlist[0][1], lmlist[0][2]
            for lm in lmlist:
                x, y = lm[1], lm[2]
                if x < x_min:
                    x_min = x
                elif x > x_max:
                    x_max = x
                if y < y_min:
                    y_min = y
                elif y > y_max:
                    y_max = y

            w = x_max - x_min
            h = y_max - y_min
            if draw:
                cv2.rectangle(image, (x_min, y_min), (x_min +  w, y_min + h), (0, 255, 0), 2)

            return (x_min, y_min, x_max, y_max)
        else:
            return 0,1,2,3