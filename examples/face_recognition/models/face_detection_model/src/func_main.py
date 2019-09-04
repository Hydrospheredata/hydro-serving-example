import dlib
import hydro_serving_grpc as hs
import numpy as np

detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor('/model/files/shape_predictor_5_face_landmarks.dat')


def detect(x):
    data = np.array(x.int_val, dtype=np.uint8)
    img = data.reshape([dim.size for dim in x.tensor_shape.dim])
    dets = detector(img, 1)
    boxes = dlib.full_object_detections()
    for i, detection in enumerate(dets):
        boxes.append(sp(img, detection))

    faces = []
    for i in range(len(boxes)):
        faces.append(dlib.get_face_chip(img, boxes[i], size=160))
    faces = np.array(faces)
    faces_shape = hs.TensorShapeProto(dim=[hs.TensorShapeProto.Dim(size=item) for item in faces.shape])
    faces_tensor = hs.TensorProto(
        dtype=hs.DT_UINT8,
        int_val=faces.flatten(),
        tensor_shape=faces_shape
    )
    return hs.PredictResponse(outputs={'faces': faces_tensor})
