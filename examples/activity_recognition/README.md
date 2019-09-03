# Activity recognition model example

This demo contains the model trained for classification of human activity (stay, sit, run, walk and riding the bike).

It is trained on [SHL dataset](http://www.shl-dataset.org)

- [Model contract](model/serving.yaml) - contains deployment configuration
- [Signature function](model/src/func_main.py) - entry point of model servable.
- [Model demo](demo/activity_recognition_demo.ipynb) - demo on how to invoke model application

## Deployment:

```commandline
cd model
hs upload
```

## Load data:
```commandline
dvc pull data/*
```

## Autoencoder:
Autoencoder is a custom model for metrics processing. It is deployed as an independent model and application. After that, it is added as a custom model in activity recognition metrics module. Autoencoder is supposed to lose accuracy when data domain changes, so it is used for data tracking.
