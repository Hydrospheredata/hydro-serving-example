# Adult model 

This demo contains the model trained on [adult dataset](https://archive.ics.uci.edu/ml/datasets/census+income) to predict whether income exceeds $50K/yr based on census data.

- [Model contract](serving.yaml) - contains deployment configuration
- [Signature function](model/src/func_main.py) - entry point of model servable.
- [Model demo](demo/Adult_demo.ipynb) - demo on how to invoke model application

Adult model is stored on remote storage, so before deploying, load it:
```commandline
dvc pull model/random-forest-adult.joblib.dvc
```

## Deployment

```commandline
cd model
hs upload
```
