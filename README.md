# Hydrosphere serving examples

This repo contains demo scenarios and pre-trained models to show Hydrosphere capabilities.

Consult Hydrosphere [documentation](https://docs.hydrosphere.io) for more information about the platform.

---
## Data Management

Some models contain dataset or artifacts for training and testing purposes. Those artifacts are managed by [dvc](https://github.com/iterative/dvc). To load data you have to:
- install `dvc`
   ```sh
   pip install dvc
   ```
- pull necessary data from dvc:
   ```sh
   dvc pull
   ``` 

---
## Python Examples

To learn more, how to deploy a python model, check out [documentation](https://docs.hydrosphere.io/quickstart/getting-started).

### [Activity recognition](examples/activity_recognition)
   Activity recognition model.
   
### [Census classification](examples/adult)
   Census classification model. 

### [Face recognition pipeline](examples/face_recognition)
   Face recognition pipeline based on FaceNet. 
   
### [Fraud detection](examples/fraud_detection)
   Fraud detection model.
   
### [MobileNet](examples/mobilenet)
   Object detection model based on MobileNet.
   
### [Titanic & XGBoost](examples/titanic_xgboost)

### [Mnist Python](examples/mnist_py)
   Hand-written digit classification model.

### [Amazon Reviews](examples/text_classification)
   Amazon reviews sentiment classification model.
