# Autoencdoer for Activity recognition model 

This demo contains the model trained for tracking data recieved for classification of human activity recognition.

It is trained on [SHL dataset](http://www.shl-dataset.org)

- [Model contract](model/serving.yaml) - contains deployment configuration
- [Signature function](model/src/func_main.py) - entry point of model servable.
- [Model demo](demo/Mnist_demo.ipynb) - demo on how to invoke Mnist model application

## How to deploy model

```commandline
cd model
hs upload
```
