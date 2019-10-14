# Activity recognition model example

This demo contains the model trained for classification of human activity (standing, sitting, running, walking and riding the bike). The data is a continuous stream of 3 sensors readings (accelerometer, gyroscope and magnetometer). Data is at [SHL dataset](http://www.shl-dataset.org)

## Folder structure:
- [Model contract](model/serving.yaml) - contains deployment configuration
- [Signature function](model/src/func_main.py) - entry point of model servable.
- [Model demo](demo/activity_recognition_demo.ipynb) - demo on how to invoke model application

## Deployment:

```commandline
cd model
hs upload
```

## Load data:
Data is managed using [dvc](https://github.com/iterative/dvc). To load data you have to:
 - install and configure  awscli: [Installation guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
     - Warning: do not forget to configure credentials for your aws account in awscli: you need to create a user
 - install `dvc[s3]` to manage s3 remote cache
 - pull necessary data from dvc:
 
```commandline
dvc pull data/*
```

## Autoencoder:
The problem of the activity recognition field is the domain gap in data: simultaneous sensors readings are different when recorded on different positions on the body. The same activity with sensors placed on the hand and the hip pocket will have some common features but will be different in overall. Our demo implements an autoencoder monitoring model, which is trained on the data collected from the hip position. So if there will be domain drift the model will recognize it and acknowledge the user.

Autoencoder is a custom model for metrics processing. It is deployed as an independent model and application. 

```commandline
cd autoencoder
hs upload
```

After that, it is added as a custom model in activity recognition model metrics module. Autoencoder is supposed to increase reconstruction loss when data domain changes.