# Fraud detection random forest model and demo example

This demo utilises a simple model to predict if transaction is fraudulent. 

It is trained on data from famous [kaggle Fraud detection competition](https://www.kaggle.com/ntnu-testimon/paysim1)

- [Model contract](model/serving.yaml) - contains deployment configuration
- [Signature function](model/src/func_main.py) - entry point of model servable
- [Model demo](demo/fraud_demo.ipynb) - demo on how to invoke Titanic model application
- [Model data](data) - fraud data
## Load data & model
```commandline
dvc pull data/*
dvc pull model/rf.joblib.pkl.dvc
```

## Deployment

```commandline
cd model
hs upload
```