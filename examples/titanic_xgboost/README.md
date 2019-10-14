# Titanic XGBoost model and demo example

This demo utilises a simple model to predict if passenger survived in Titanic disaster given information about his age, sex, passenger's class, ticket fare and number of parent/children abroad the Titanic.

It is trained on data from famous [kaggle Titanic competition](https://www.kaggle.com/c/titanic/overview)

- [Model contract](model/serving.yaml) - contains deployment configuration
- [Signature function](model/src/func_main.py) - entry point of model servable
- [Model demo](demo/titanic_demo.ipynb) - demo on how to invoke Titanic model application
- [Model training](model/train) - code to train model
- [Model data](data) - training and test data

## Load data
Data is managed using [dvc](https://github.com/iterative/dvc). To load data you have to:
 - install and configure  awscli: [Installation guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
     - Warning: do not forget to configure credentials for your aws account in awscli: you need to create a user
 - install `dvc[s3]` to manage s3 remote cache
 - pull necessary data from dvc:

```commandline
dvc pull data/*
```

## Training

```commandline
pip install -r requirements.txt
cd model/train
python train.py
```

## Deployment
```commandline
cd model
hs upload
```