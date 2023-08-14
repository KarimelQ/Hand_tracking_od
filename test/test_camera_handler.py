import sys, os
sys.path.append(os.path.join(os.getcwd(),  'Development', 'pipeline'))
sys.path.append(os.path.join(os.getcwd(), os.pardir, 'Development', 'pipeline'))

import unittest
import camera_handler 

class TestCameraHandler(unittest.TestCase):
    def test_camera(self):
        CH = camera_handler.CameraHandler()
        image = CH.take_picture()
        self.assertEqual(image.shape, (CH.height, CH.width, CH.channels))
        return 1

if __name__ == '__main__':
    unittest.main()