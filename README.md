# Hydrosphere serving examples

This repo contains demo scenarios and pre-trained models to show Hydrosphere capabilities.

Consult [documentation](https://docs.hydrosphere.io) for more information about the platform.

## Data Management

Some models contain dataset or artifacts for training and testing purposes. Those artifacts are managed by [dvc](https://github.com/iterative/dvc). To load data you have to:
- Install `dvc` package.
   ```sh
   pip install dvc
   ```
- Pull all or necessary data from the remote storage.
   ```sh
   dvc pull examples/adult/data/adult.csv.dvc # load specific file
   dvc pull # load all remote files
   ``` 

## Python Examples

To learn more, how to deploy a python model, check out [documentation](https://docs.hydrosphere.io/quickstart/getting-started).

* [Activity recognition model](examples/activity_recognition).
* [Census classification model](examples/adult).
* [Face recognition pipeline based on FaceNet](examples/face_recognition).
* [Fraud detection model](examples/fraud_detection). 
* [Object detection model based on MobileNet](examples/mobilenet).  
* [Titanic survival classification model](examples/titanic_xgboost).
* [Hand-written digit classification model](examples/mnist_py).
* [Amazon reviews sentiment classification model](examples/text_classification).
