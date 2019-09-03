# Mnist model and demo example

This demo contains the model trained for mnist digit classification.

It is trained on [mnist dataset](http://yann.lecun.com/exdb/mnist/)

- [Model contract](model/serving.yaml) - contains deployment configuration
- [Signature function](model/src/func_main.py) - entry point of model servable.
- [Model demo](demo/python_mnist_demo.ipynb) - demo on how to invoke Mnist model application

## How to deploy model

```commandline
cd model
hs upload
```