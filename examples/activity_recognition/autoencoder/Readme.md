# Autoencdoer for Activity recognition model 

This demo contains the model trained for tracking data recieved for classification of human activity recognition.

It is trained on [SHL dataset](http://www.shl-dataset.org)

- [Model contract](serving.yaml) - contains deployment configuration
- [Signature function](src/func_main.py) - entry point of model servable.


## How to deploy model

```commandline
cd model
hs upload
```
