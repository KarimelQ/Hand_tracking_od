#ifndef CAMERA_HANDLER_H
#define CAMERA_HANDLER_H

#include <opencv2/opencv.hpp>
#include <string>
#include <vector>

class Camera
{
public:
    // Constructor
    Camera(int width, int height);

    // Destructor
    ~Camera();

    // Member function to take a picture
    cv::Mat takePicture();

    bool isOpened();

    // Member function to take a picture
    std::vector<cv::Mat> take_shuffle(int n);

private:
    cv::VideoCapture cap;
};

#endif // CAMERA_HANDLER_H