# Titanic survival classification model

This demo utilises a simple model to predict if passenger survived in Titanic disaster given information about his age, sex, passenger's class, ticket fare and number of parent/children abroad the Titanic.

It is trained on data from famous the Kaggle [Titanic competition](https://www.kaggle.com/c/titanic/overview).

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

## Model deployment

To deploy a model, create an application from it. You can do it either from the UI, or by using our Python SDK.

```py
from hydrosdk.application import ApplicationBuilder, ExecutionStageBuilder
from hydrosdk import Cluster, ModelVersion
from grpc import ssl_channel_credentials

cluster = Cluster(
    http_address="<hydrosphere-http-address>",
    grpc_address="<hydrosphere-grpc-address>",
    ssl=True,                                       # turn off, if your Hydrosphere instance doesn't have
    grpc_credentials=ssl_channel_credentials(),     # TLS certificates installed
)

mv = ModelVersion.find(cluster, "titanic_xgboost", 1)
mv.lock_till_released()
stage = ExecutionStageBuilder().with_model_variant(mv, 100).build()
app = ApplicationBuilder(cluster, "titanic_xgboost").with_stage(stage).build()
app.lock_while_starting()
```
