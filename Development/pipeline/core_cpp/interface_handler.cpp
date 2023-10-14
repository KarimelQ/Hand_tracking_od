#include "interface_handler.h"

BlackBoxViewer::BlackBoxViewer() {
    blackBox_ = cv::Mat(480, 640, CV_8UC3, cv::Scalar(0, 0, 0));
    windowName_ = "Black Box Viewer";
    cv::namedWindow(windowName_);
}

BlackBoxViewer::~BlackBoxViewer() {
    cv::destroyWindow(windowName_);
}

void BlackBoxViewer::showPosition(const cv::Point& position) {
    cv::Mat blackBoxCopy = blackBox_.clone();
    cv::circle(blackBoxCopy, position, 6, cv::Scalar(0, 0, 255), -1); // Draw a red circle at the position
    cv::imshow(windowName_, blackBoxCopy);
    cv::waitKey(10); // Show the image for a short time (milliseconds)
}
