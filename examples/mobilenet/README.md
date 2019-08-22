# Mobilenet model and demo example

This demo utilises 

It is trained on [ImageNet data](http://www.image-net.org)

- [Model contract](model/serving.yaml) - contains deployment configuration
- [Signature function](model/src/func_main.py) - entry point of model servable
- [Model demo](demo/Mobile_net_demo.ipynb) - demo on how to invoke mobilenet model application

## How to load data
```commandline
dvc pull data/*
```

## How to deploy model
```commandline
cd model
hs upload
```