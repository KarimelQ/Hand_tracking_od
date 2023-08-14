import tensorflow as tf
import numpy as np
import os
import object_detection
import tensorflow as tf
from object_detection.utils import config_util,label_map_util
from object_detection.protos import pipeline_pb2
from google.protobuf import text_format
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util
import cv2

class HandDetector:
    def __init__(self,config_path,checkpoint_path):
        config_path = "/home/karimelq/Documents/Personal_work/Gestures_scratch/workspace/models/finetuned_ssd_model/pipeline.config"
        checkpoint_path = "/home/karimelq/Documents/Personal_work/Gestures_scratch/workspace/models/finetuned_ssd_model"
        self.detection_model = self.get_model(config_path,checkpoint_path)
        # TODO: add inference with simulated input to avoid stopping in real inference
        self.get_bounding_box(np.zeros(shape=(480,640,3)),1)

    def get_model(self,config_path,checkpoint_path):
        configs = config_util.get_configs_from_pipeline_file(config_path)
        detection_model = model_builder.build(model_config=configs['model'], is_training=False)
        # Restore checkpoint
        ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
        ckpt.restore(os.path.join(checkpoint_path , 'ckpt-11')).expect_partial()
        return detection_model
    
    @tf.function
    def detect(self, image):
        image, shapes = self.detection_model.preprocess(image)
        prediction_dict = self.detection_model.predict(image, shapes)
        detections = self.detection_model.postprocess(prediction_dict, shapes)
        return detections

    def get_bounding_box(self, frame, threshold):
        input_tensor = tf.convert_to_tensor(np.expand_dims(frame, 0), dtype=tf.float32)
        detections = self.detect(input_tensor)

        if detections['detection_scores'][0].numpy()[0] > threshold:
            ymin, xmin, ymax, xmax = detections['detection_boxes'][0].numpy()[0]
            height, width, _ = frame.shape
            xmin = int(xmin * width)
            xmax = int(xmax * width)
            ymin = int(ymin * height)
            ymax = int(ymax * height)
            return 1, ymin, xmin, ymax, xmax
        else:
            return 0, 0, 0, 0, 0

    def get_hand_position(self, frame, threshold = 0):
        input_tensor = tf.convert_to_tensor(np.expand_dims(frame, 0), dtype=tf.float32)
        detections = self.detect(input_tensor)

        # print(detections['detection_scores'][0].numpy()[0])
        if detections['detection_scores'][0].numpy()[0] > threshold:
            ymin, xmin, ymax, xmax = detections['detection_boxes'][0].numpy()[0]
            height, width, _ = frame.shape
            xmin = int(xmin * width)
            xmax = int(xmax * width)
            ymin = int(ymin * height)
            ymax = int(ymax * height)
            return 640-int((xmin+xmax)/2),int((ymin+ymax)/2)
        else:
            return (0,0)
        

    def draw_bounding_box(self, frame):
        _ , ymin, xmin, ymax, xmax = self.get_bounding_box(frame,0)
        frame = cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        return frame