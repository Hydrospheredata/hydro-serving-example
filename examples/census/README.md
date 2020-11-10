# Census classification model 

This folder contains a model for a classification task based on the [Adult Dataset](https://www.kaggle.com/wenruliu/adult-income-dataset). 

## Directory structure

- `data` — Folder contains data to train the model.
- `demo` — Folder contains a sample Jupyter notebook for invoking a deployed model.
- `model` — Folder contains model artifacts, ready to be uploaded to the Hydrosphere. 
- `ops` — Folder contains models' training script.

## Prerequisites

In order to upload the model to the Hydrosphere you will need the [Hydrosphere CLI](https://docs.hydrosphere.io/quickstart/installation/cli).

```sh
pip install hs
```

Once you've installed CLI, add your Hydrosphere cluster.

```sh
hs cluster add --server http://localhost --name local
hs cluster use local
```

## Model upload

To upload the model, follow below steps.

```sh
cd model
hs upload
```
