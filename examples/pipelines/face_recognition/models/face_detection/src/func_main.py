import dlib
import numpy as np


detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor('/model/files/shape_predictor_5_face_landmarks.dat')


def detect(x):
    dets = detector(x, 1)
    boxes = dlib.full_object_detections()
    for i, detection in enumerate(dets):
        boxes.append(sp(x, detection))
    faces = []
    for i in range(len(boxes)):
        faces.append(dlib.get_face_chip(x, boxes[i], size=160))
    return {"faces": np.array(faces).astype('uint8')}
