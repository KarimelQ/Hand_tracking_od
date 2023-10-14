#ifndef HAND_DETECTOR_HPP
#define HAND_DETECTOR_HPP

#include <opencv2/opencv.hpp>
#include <tensorflow/lite/interpreter.h>
#include <tensorflow/lite/kernels/register.h>
#include <tensorflow/lite/model.h>

#define NEW_WIDTH  320
#define NEW_HEIGHT 320
#define HAND_TRESHOLD 0.6

class HandDetector {
public:
    HandDetector(const char *model_path);

    const cv::Mat& getImage() const;

    std::tuple<cv::Point, cv::Point > getBoundingBox(cv::Mat image, float threshold , bool draw_bbox);
    void drawBoundingBox(cv::Mat image, cv::Point pt1, cv::Point pt2);
    cv::Point getHandPosition() const;
    cv::Point findMidpoint(cv::Mat image);
    
    std::unique_ptr<tflite::FlatBufferModel> model;
    tflite::ops::builtin::BuiltinOpResolver resolver;
    std::unique_ptr<tflite::Interpreter> interpreter;
};

#endif // HAND_DETECTOR_HPP
