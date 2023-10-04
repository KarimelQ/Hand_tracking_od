#ifndef INTERFACE_HANDLER_H
#define INTERFACE_HANDLER_H

#include <opencv2/opencv.hpp>

class BlackBoxViewer {
public:
    BlackBoxViewer();
    ~BlackBoxViewer();

    void showPosition(const cv::Point& position);

private:
    cv::Mat blackBox_;
    std::string windowName_;
};

#endif // INTERFACE_HANDLER_H
