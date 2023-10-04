#include <iostream>
#include "camera_handler.h"
#include "hand_detector.h"
#include <chrono>
#include <thread>
#include "interface_handler.h"

int main(int argc, char *argv[]) {
    Camera camera(640,480);
    const char *model_path = "../../../Model/model_with_metadata.tflite";
    HandDetector detector(model_path);
    if (!camera.isOpened()) {
        std::cout << "Camera initialization failed!" << std::endl;
        return -1;
    }

    BlackBoxViewer viewer;
    cv::Point pt;
    while (true) {
        cv::Mat image = camera.takePicture();
        // cv::Mat image = cv::imread("/home/karimelq/Documents/Dev/Gestures_scratch/workspace/images/test/hand40.jpg");
        pt = detector.findMidpoint(image);
        // std::cout <<"x" << pt.x <<"y "<< pt.y<<std::endl;
        viewer.showPosition(pt);
    }
}
