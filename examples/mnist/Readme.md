# Mnist tensorflow model and demo example

This demo contains the model trained for mnist digit classification.

It is trained on [mnist dataset](http://yann.lecun.com/exdb/mnist/)

- [Model configuration](model/) - contains saved tensorflow model and metafiles
- [Medel define and train file](basic-api.py) - defines model architecture, hyperparameters. Preprocess and trains the model
- [Model demo](demo/Mnist_demo.ipynb) - demo on how to invoke Mnist model application


## How to train XGBoost model

```commandline
pip install -r requirements.txt
cd model
python basic_api.py
```

## How to deploy model

```commandline
cd model
hs upload
```