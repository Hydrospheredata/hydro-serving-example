# Fraud detection random forest model and demo example

This demo utilises a simple model to predict if transaction is fraudulent. 

It is trained on data from famous [kaggle Fraud detection competition](https://www.kaggle.com/ntnu-testimon/paysim1)

- [Model contract](model/serving.yaml) - contains deployment configuration
- [Signature function](model/src/func_main.py) - entry point of model servable
- [Model demo](demo/Fraud_Demo.ipynb) - demo on how to invoke Titanic model application
- [Model data](data) - fraud data
## How to load data
```commandline
cd data
dvc run -d s3://hydrosphere-examples/data/fraud_data.csv
          -o fraud_data.csv
          aws s3 cp s3://hydrosphere-examples/data/fraud_data.csv fraud_data.csv
```
## How to deploy model

```commandline
cd model
hs upload
```