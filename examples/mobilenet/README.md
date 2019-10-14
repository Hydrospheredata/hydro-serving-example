# Mobilenet model and demo example

This demo utilises 

It is trained on [ImageNet data](http://www.image-net.org)

- [Model contract](model/serving.yaml) - contains deployment configuration
- [Signature function](model/src/func_main.py) - entry point of model servable
- [Model demo](demo/mobilenet_demo.ipynb) - demo on how to invoke mobilenet model application

## Load data
Data is managed using [dvc](https://github.com/iterative/dvc). To load data you have to:
 - install and configure  awscli: [Installation guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
     - Warning: do not forget to configure credentials for your aws account in awscli: you need to create a user
 - install `dvc[s3]` to manage s3 remote cache
 - pull necessary data from dvc:
```commandline
dvc pull data/*
```

## Deployment
```commandline
cd model
hs upload
```