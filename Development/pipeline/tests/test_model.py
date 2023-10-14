import unittest
from core_py.hand_detector import HandDetector
import hand_detector_wrapped
import cv2
import math

TOLERANCE_MAX = 2 # 2 pixels of max tolerance 

class TestSum(unittest.TestCase):
    def test_quantized_vs_float(self):
        # get CPP for quantized model result
        hd = hand_detector_wrapped.HandDetector('/home/karimelq/Documents/Dev/Handtracker/Development/Model/model.tflite')
        position = hd.Inference()
        x_q = position[0]
        y_q = position[1]


        # get python model result
        image = cv2.imread('test_image.jpg')
        config_path = "/home/karimelq/Documents/Dev/Handtracker/workspace/models/finetuned_ssd_model/pipeline.config"
        cpt_path = "/home/karimelq/Documents/Dev/Handtracker/workspace/models/finetuned_ssd_model"
        HD = HandDetector(config_path, cpt_path)
        x_f, y_f  = HD.get_hand_position(image,0.7)

        assert math.isclose(int(x_q), int(x_f), abs_tol=TOLERANCE_MAX)
        assert math.isclose(int(y_q), int(y_f), abs_tol=TOLERANCE_MAX)

    if __name__ == '__main__':
        unittest.main()
