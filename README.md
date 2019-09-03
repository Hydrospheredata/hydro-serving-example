# Hydrosphere serving examples
This repo contains various demo scenarios and pre-trained models.

[Hydrosphere documentation]( https://hydrosphere.io/serving-docs/latest/index.html)

---------

## Python Runtime: 
[Python serving documentation](https://hydrosphere.io/serving-docs/latest/tutorials/python.html)
###  [Acitvity recognition](examples/activity_recognition)
   Activity recognition model
   
### [Adult](examples/adult)

### [Face recognition pipeline](examples/face_recognition)
   Face recognition pipeline based on facenet
   
### [Fraud detection](examples/fraud_detection)
   Fraud detection model
   
### [Mobilenet](examples/mobilenet)
   Object detection model based on Mobilenet
   
### [Titanic prediction](examples/titanic_xgboost)

### [Mnist Python](examples/python_mnist)
   Digit classification model


## Tensorflow Runtime:
[Tensorflow serving documentation](https://hydrosphere.io/serving-docs/latest/tutorials/tensorflow.html)
### [Mnist Tensorflow](examples/mnist)
   Digit classification model
   
## Spark Runtime:
### [Binarizer](examples/binarizer)

# Data Management
Some models contain dataset for training/testing purposes. This data is stored on s3 bucket: s3://hydrosphere-examples. 
Data is managed using [dvc](https://github.com/iterative/dvc). To load data you have to:
 - install and configure  awscli: [Installation guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
 - install dvc[s3] to manage s3 remote cache
 - pull necessary data from dvc:
 
    to pull all data:
     ```commandline
    dvc pull
    ```
    
     to pull data for certain model:
     ```commandline
    dvc pull examples/MODEL_NAME/data/*
    ```
 