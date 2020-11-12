# Amazon Review Sentiment Analysis

This demo utilizes a model trained on an Amazon reviews dataset to predict review's sentiment. 

## Directory structure

- `data` — Folder contains data to train the model.
- `demo` — Folder contains a sample Jupyter notebook for invoking a deployed model.
- `models` — Folder contains model artifacts, ready to be uploaded to the Hydrosphere. 

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
cd models/tokenizer
hs upload
cd ../estimator
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

mv1 = ModelVersion.find(cluster, "amazon_tokenizer", 1)
mv1.lock_till_released()
mv2 = ModelVersion.find(cluster, "amazon_estimator", 1)
mv2.lock_till_released()
stage1 = ExecutionStageBuilder().with_model_variant(mv1, 100).build()
stage2 = ExecutionStageBuilder().with_model_variant(mv2, 100).build()
app = ApplicationBuilder(cluster, "amazon_sentiment") \
    .with_stage(stage1) \
    .with_stage(stage2) \
    .build()
app.lock_while_starting()
```
