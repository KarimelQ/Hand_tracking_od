#include <opencv2/opencv.hpp>
#include "camera_handler.h"
#include <vector>

Camera::Camera(int width, int height) {
    cap.open(0); // Open the default camera (index 0)
    if (!cap.isOpened()) {
        std::cout << "Error: Unable to open the camera." << std::endl;
    }
    // Set custom image size
    cap.set(cv::CAP_PROP_FRAME_WIDTH, width);
    cap.set(cv::CAP_PROP_FRAME_HEIGHT, height);
}

Camera::~Camera() {
    cap.release(); // Release the camera when the object is destroyed
}

bool Camera::isOpened(){
    return cap.isOpened();
}

cv::Mat Camera::takePicture() {
    cv::Mat frame;
    cap.read(frame); // Capture a frame from the camera

    if (frame.empty()) {
        throw std::runtime_error("Error: Unable to capture the frame.");
    }
    return frame;
}

std::vector<cv::Mat> Camera::take_shuffle(int n) {
    std::vector<cv::Mat> frames;
    for (int i = 0; i < n; ++i) {
        frames.push_back(takePicture()); // Call the takePicture method from within take_shuffle
    }
    return frames;
}