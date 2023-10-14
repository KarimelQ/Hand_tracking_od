#include <iostream>
// #include "camera_handler.h"
#include "hand_detector.h"
#include <chrono>
#include <thread>
// #include "interface_handler.h"
// #include <pybind11/pybind11.h>

int main(int argc, char *argv[]) {
    // Camera camera(640,480);
    // const char *model_path = "../../../Model/model_with_metadata.tflite";
    HandDetector detector(model_path);

    cv::Mat image = cv::imread("../test_image.jpg"); // Replace "your_image.jpg" with the path to your image file
    cv::Point pt;
    // detector.getBoundingBox()
    
    // cv::imshow("Image", image);
    // cv::waitKey(0);
    // cv::destroyWindow("Image");

    detector.getBoundingBox(image, 0.8, true);
    return 0;
}
