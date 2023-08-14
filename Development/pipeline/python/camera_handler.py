#################################################################################
#
#   24-09-2022
#   KELQ
#
#################################################################################

import cv2
import os
from pathlib import Path
import os, shutil
from shutil import copy2

class CameraHandler():
    def __init__(self, grayscale=False, activate=True) -> None:
        """
        function
        input :
        output :
        """
        if activate:
            self.camera_activate = True
            self.camera = cv2.VideoCapture(0)
            self.height = 480
            self.width  = 640
            self.channels = 1 if grayscale else 3

    def take_picture(self):
        """
        function
        input :
        output :
        """
        if(self.camera_activate == False):
            raise TypeError(" Camera desactivated, please activate")

        #130ms per picture
        s, img = self.camera.read()
        if s:    # frame captured without any errors
            return img
        else:
            raise TypeError(" Error taking picture")


    def take_shuffle(self, nb_images):
        """
        function
        input :
        output :
        """
        return [self.take_picture() for _ in range(nb_images)]

    # done outside to not impact time when taking picture 
    def rgb_to_grayscale(self, img):
        """
        function 
        input :
        output :

        """
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def images_to_video(self, images, video_number, video_name):
        """
        function 
        input :
        output :
        """
        out = cv2.VideoWriter(
            f'{video_name}.avi',
            cv2.VideoWriter_fourcc(*'DIVX'),
            15,
            (self.width, self.height),
        )
        for i in range(len(images)):
            out.write(images[i])
        out.release()

        destination_path = f'{os.getcwd()}/data/video_{video_number}'
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

    def video_to_images(self, src_path):
        """
        function 
        input :
        output :
        """
        vidcap = cv2.VideoCapture(f'{src_path}/video.avi')
        success,image = vidcap.read()
        count = 0
        while success:
            path = os.path.abspath(src_path)
            cv2.imwrite(src_path+"/frame%d.jpg" % count, image)
            success,image = vidcap.read()
            count += 1
        return count

    def camera_enable(self, state):
        """
        function
        input :
        output :

        """
        if(state==True):
            if(self.camera_activate == False):
                self.camera = cv2.VideoCapture(0)
                self.camera_activate = True
        else:
            self.camera.release()
            self.camera_activate = False