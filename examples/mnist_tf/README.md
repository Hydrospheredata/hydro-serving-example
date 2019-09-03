# Mnist tensorflow model and demo example

This demo contains the model trained for mnist digit classification.

It is trained on [mnist dataset](http://yann.lecun.com/exdb/mnist/)

- [Model configuration](model/) - contains saved tensorflow model and metafiles
- [Model define and train file](train_mnist.py) - defines model architecture, hyperparameters. Preprocess and trains the model
- [Model demo](demo/mnist_demo.ipynb) - demo on how to invoke Mnist model application


## Training:

```commandline
cd model
python basic_api.py
```

## Deployment:

```commandline
cd model
hs upload --name mnist_tf --runtime hydrosphere/serving-runtime-tensorflow-1.13.1:dev
```
