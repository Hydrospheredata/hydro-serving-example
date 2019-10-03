# Hydrosphere serving examples
This repo contains demo scenarios and pre-trained models to show Hydro Serving capabilities.

[Hydrosphere documentation]( https://hydrosphere.io/serving-docs/latest/index.html)

-----

## Data Management
Some models contain dataset for training/testing purposes. This data is stored on s3 bucket: s3://hydrosphere-examples. 
Data is managed using [dvc](https://github.com/iterative/dvc). To load data you have to:
 - install and configure  awscli: [Installation guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
 - install `dvc[s3]` to manage s3 remote cache
 - pull necessary data from dvc:
 
    to pull all data:
     ```commandline
    dvc pull
    ```
    
     to pull data for certain model:
     ```commandline
    dvc pull examples/MODEL_NAME/data/*
    ```
 

---------
## Python Runtime Examples: 
[Python serving documentation](https://hydrosphere.io/serving-docs/latest/tutorials/python.html)
###  [Acitvity recognition](examples/activity_recognition)
   Activity recognition model
   
### [Census Dataset](examples/adult)

### [Face recognition pipeline](examples/face_recognition)
   Face recognition pipeline based on facenet
   
### [Fraud detection](examples/fraud_detection)
   Fraud detection model
   
### [Mobilenet](examples/mobilenet)
   Object detection model based on Mobilenet
   
### [Titanic & XGBoost](examples/titanic_xgboost)

### [Mnist Python](examples/mnist_py)
   Digit classification model

### [Amazon Reviews](examples/text_classification)
   [Amazon customer reviews](https://www.kaggle.com/bittlingmayer/amazonreviews) (input text) and star ratings (output labels)  for sentiment prediction
 

## Tensorflow Runtime Examples:
[Tensorflow serving documentation](https://hydrosphere.io/serving-docs/latest/tutorials/tensorflow.html)
### [Mnist Tensorflow](examples/mnist_tf)
   Digit classification model
   
## Spark Runtime Examples:
### [Binarizer](examples/binarizer)

