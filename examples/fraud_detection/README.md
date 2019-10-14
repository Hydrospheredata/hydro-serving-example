# Fraud detection random forest model and demo example

This demo utilises a simple model to predict if transaction is fraudulent. 

It is trained on data from famous [kaggle Fraud detection competition](https://www.kaggle.com/ntnu-testimon/paysim1)

- [Model contract](model/serving.yaml) - contains deployment configuration
- [Signature function](model/src/func_main.py) - entry point of model servable
- [Model demo](demo/fraud_demo.ipynb) - demo on how to invoke Titanic model application
- [Model data](data) - fraud data
## Load data & model
Data is managed using [dvc](https://github.com/iterative/dvc). To load data you have to:
 - install and configure  awscli: [Installation guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
     - Warning: do not forget to configure credentials for your aws account in awscli: you need to create a user
 - install `dvc[s3]` to manage s3 remote cache
 - pull necessary data from dvc:
 
```commandline
dvc pull data/*
dvc pull model/rf.joblib.pkl.dvc
```

## Deployment

```commandline
cd model
hs upload
```