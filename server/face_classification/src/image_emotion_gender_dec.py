import sys

import cv2
from keras.models import load_model
import numpy as np

from .utils.datasets import get_labels
from .utils.inference import detect_faces
from .utils.inference import draw_text
from .utils.inference import draw_bounding_box
from .utils.inference import apply_offsets
from .utils.inference import load_detection_model
from .utils.inference import load_image
from .utils.preprocessor import preprocess_input

from tensorflow import Graph, Session

import os


def gender_emotion_dec(image_path):
    # parameters for loading data and images
    # image_path = sys.argv[1]


    dir = '/home/ec2-user/untitled6/face_classification'


    detection_model_path = dir + '/trained_models/detection_models/haarcascade_frontalface_default.xml'

    emotion_model_path = dir + '/trained_models/emotion_models/fer2013_mini_XCEPTION.102-0.66.hdf5'
    gender_model_path = dir + '/trained_models/gender_models/simple_CNN.81-0.96.hdf5'
    emotion_labels = get_labels('fer2013')
    gender_labels = get_labels('imdb')
    font = cv2.FONT_HERSHEY_SIMPLEX

    # hyper-parameters for bounding boxes shape
    gender_offsets = (30, 60)
    gender_offsets = (10, 10)
    emotion_offsets = (20, 40)
    emotion_offsets = (0, 0)

    # loading models
    face_detection = load_detection_model(detection_model_path)
    graph1 = Graph()
    with graph1.as_default():
        session1 = Session()
        with session1.as_default():
            emotion_classifier = load_model(emotion_model_path, compile=False)
            gender_classifier = load_model(gender_model_path, compile=False)


            # getting input model shapes for inference
            emotion_target_size = emotion_classifier.input_shape[1:3]
            gender_target_size = gender_classifier.input_shape[1:3]

            # loading images
            rgb_image = load_image(image_path, grayscale=False)
            gray_image = load_image(image_path, grayscale=True)
            gray_image = np.squeeze(gray_image)
            gray_image = gray_image.astype('uint8')

            faces = detect_faces(face_detection, gray_image)
            if len(faces) == 0:
                print("No face Detected, Please try again")
                return [""]*4
            x1, x2, y1, y2 = apply_offsets(faces[0], gender_offsets)
            rgb_face = rgb_image[y1:y2, x1:x2]

            x1, x2, y1, y2 = apply_offsets(faces[0], emotion_offsets)
            gray_face = gray_image[y1:y2, x1:x2]

            try:
                rgb_face = cv2.resize(rgb_face, (gender_target_size))
                gray_face = cv2.resize(gray_face, (emotion_target_size))
            except:
                pass

            rgb_face = preprocess_input(rgb_face, False)
            rgb_face = np.expand_dims(rgb_face, 0)
            gender_prediction = gender_classifier.predict(rgb_face)
            gender_label_arg = np.argmax(gender_prediction)
            gender_text = gender_labels[gender_label_arg]
            print("test print: ",len(gender_prediction),gender_label_arg)
            gender_p = str(gender_prediction[0][gender_label_arg])

            gray_face = preprocess_input(gray_face, True)
            gray_face = np.expand_dims(gray_face, 0)
            gray_face = np.expand_dims(gray_face, -1)
            p = emotion_classifier.predict(gray_face)
            emotion_label_arg = np.argmax(p)
            emotion_text = emotion_labels[emotion_label_arg]
            emotion_p = str(p[0][emotion_label_arg])

            return [emotion_text,gender_text,emotion_p,gender_p]
    # if gender_text == gender_labels[0]:
    #     color = (0, 0, 255)
    # else:
    #     color = (255, 0, 0)

#     draw_bounding_box(face_coordinates, rgb_image, color)
#     draw_text(face_coordinates, rgb_image, gender_text, color, 0, -20, 1, 2)
#     draw_text(face_coordinates, rgb_image, emotion_text, color, 0, -50, 1, 2)
#
# bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
# cv2.imwrite('../images/predicted_test_image.png', bgr_image)
