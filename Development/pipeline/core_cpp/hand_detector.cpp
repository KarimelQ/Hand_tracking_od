#include "hand_detector.h"
#include <tensorflow/lite/interpreter.h>
#include <tensorflow/lite/kernels/register.h>
#include <tensorflow/lite/model.h>
#include <tuple>
#include <vector>

std::tuple<cv::Point, cv::Point > Output_to_points(float *output, int original_w, int original_h){
    float ymin,xmin, ymax, xmax;
    float ratio_x,ratio_y;  


    ratio_x = original_w/static_cast<float>(NEW_WIDTH);  //640/320 = 2
    ratio_y = original_h/static_cast<float>(NEW_HEIGHT); //480/320 = 1.5

    ymin = output[0]*NEW_HEIGHT*ratio_y;
    ymax = output[2]*NEW_HEIGHT*ratio_y;
    
    xmin = output[1]*NEW_WIDTH*ratio_x;
    xmax = output[3]*NEW_WIDTH*ratio_x;

    cv::Point pt1(xmin, ymin);
    cv::Point pt2(xmax, ymax);

    return std::make_tuple(pt1, pt2);
}

HandDetector::HandDetector(const char *model_path) {
    model = tflite::FlatBufferModel::BuildFromFile(model_path);

    if (!model) {
        assert("Please, give correct path for model");
    }

    tflite::InterpreterBuilder builder(*model, resolver);
    builder(&interpreter);

    if (!interpreter) {
        assert("Failed to load interpreter");
    }
}

std::tuple<cv::Point, cv::Point > HandDetector::getBoundingBox(cv::Mat image, float threshold, bool draw_bbox) {
    cv::Mat floatImage;
    cv::Mat res_image;

    cv::Size newSize(NEW_WIDTH, NEW_HEIGHT);
    cv::resize(image, res_image, newSize); //src , dest

    res_image.convertTo(floatImage, CV_32F, 2.0 / 255.0, -1.0);
    // std::cout << "input image dimensions: " << floatImage.total()<< " x "<< image.elemSize() <<std::endl;
    
    // Allocate tensors
    if (interpreter->AllocateTensors() != kTfLiteOk) {
        assert("Failed to allocate tensors");
    }

    std::memcpy(interpreter->typed_input_tensor<float>(0), floatImage.data, floatImage.total()*floatImage.elemSize());

    // std::cout <<"Inference ... "<< std::endl;
    interpreter->Invoke();
    // std::cout <<"Inference done."<< std::endl;
    
    float* confidence = interpreter->typed_output_tensor<float>(0);

    float* output = interpreter->typed_output_tensor<float>(1);
    // for (int i=0; i<4;i++){
    //     std::cout << output[i] << std::endl;
    // }

    cv::Point pt1,pt2;
    std::tie(pt1, pt2) = Output_to_points(output, image.cols, image.rows);
    // std::cout <<"x" << pt1.x <<"y "<< pt1.y<<std::endl;
    if(confidence[0] > threshold)
    {
        if(draw_bbox){
            drawBoundingBox(image, pt1, pt2);
        }
        return std::make_tuple(pt1, pt2);
    }

    cv::Point originPoint(0, 0);
    return std::make_tuple(originPoint, originPoint);
}

void HandDetector::drawBoundingBox(cv::Mat image, cv::Point pt1, cv::Point pt2) {
    cv::Scalar color(0, 255, 0);  // Green color
    int thickness = 2;
    cv::rectangle(image, pt1, pt2, color, thickness);
    cv::imshow("image with Box", image);
    cv::waitKey(0);
    cv::destroyAllWindows();
}

cv::Point HandDetector::findMidpoint(cv::Mat image) {
    cv::Point pt1,pt2;

    std::tie(pt1, pt2) = getBoundingBox(image, HAND_TRESHOLD, false);

    float midX = (pt1.x + pt2.x) / 2;
    float midY = (pt1.y + pt2.y) / 2;
    return cv::Point(640.0-midX, midY);
}