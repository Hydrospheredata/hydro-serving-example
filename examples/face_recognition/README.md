#Face detection and face recognition pipeline
This model consists of two stages:
1. face detection - detecting faces in img
2. face recognition - classifying faces (uses [facenet](https://github.com/davidsandberg/facenet) model for face embeddings and KNN classifier trained on [lfw dataset](http://vis-www.cs.umass.edu/lfw/))

## Pipeline structure:
![model](face_recognition.png)

## Face detection: 
- [Model contract](models/face_detection_model/serving.yaml) - contains deployment configuration
- [Signature function](models/face_detection_model/src/func_main.py) - entry point of model servable

### Deployment
```commandline
cd models/face_detection_model
hs upload
```

## Face recognition:
- [Model contract](models/facenet_model/serving.yaml) - contains deployment configuration
- [Signature function](models/facenet_model/src/func_main.py) - entry point of model servable
- [LFW_KNN_Classifier](models/facenet_model/lfw_classifier.pkl)
- [Pretrained facenet model](models/facenet_model/20180402-114759.pb)

### Deployment
```commandline
cd models/facenet_model
hs upload
```
