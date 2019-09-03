# Binarizer spark model 

This demo contains the model (spark) for binarization of input value. If value is smaller than threshold it returns 0, otherwise 1


- [Model demo](demo/Binarizer_demo.ipynb) - demo on how to invoke model application

## Deployment:

```commandline
cd model
hs upload --runtime hydrosphere/serving-runtime-spark-2.1.2:dev
```
