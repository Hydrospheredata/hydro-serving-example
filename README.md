# Hydrosphere examples

This repo contains demo scenarios and pre-trained models to show Hydrosphere capabilities.

## Data and artifacts management

Some models contain dataset or artifacts for training and testing purposes. Those artifacts are managed by [dvc](https://github.com/iterative/dvc). 

To load data follow below steps.
- Install `dvc` package.
   ```sh
   pip install dvc
   ```
- Pull all or necessary data from the remote storage.
   ```sh
   dvc pull examples/adult/data/adult.csv.dvc # load specific file
   dvc pull # load all remote files
   ``` 

## Python examples

To learn more, how to deploy a python model, check out our [getting started](https://docs.hydrosphere.io/quickstart/getting-started) guide.

* [Activity recognition model](examples/activity_recognition).
* [Census classification model](examples/adult).
* [Face recognition pipeline based on FaceNet](examples/face_recognition).
* [Fraud detection model](examples/fraud_detection). 
* [Object detection model based on MobileNet](examples/mobilenet).  
* [Titanic survival classification model](examples/titanic_xgboost).
* [Hand-written digit classification model](examples/mnist_py).
* [Amazon reviews sentiment classification model](examples/text_classification).
