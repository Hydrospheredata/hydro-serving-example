# Face recognition pipeline based on FaceNet

This model consists of two stages:
1. Face detection - detecting faces on an image
1. Face recognition - classifying detected faces (uses [facenet](https://github.com/davidsandberg/facenet) model for face embeddings and KNN classifier trained on [lfw dataset](http://vis-www.cs.umass.edu/lfw/))

## Directory structure:

- `demo` — Folder contains a sample Jupyter notebook for invoking a deployed model.
- `models` — Folder contains two model artifacts, ready to be uploaded to the Hydrosphere. 

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

To upload the models, follow below steps.

```sh
cd models/face_detection
hs upload
cd ../face_recognition
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

mv1 = ModelVersion.find(cluster, "face_detection", 1)
mv1.lock_till_released()
mv2 = ModelVersion.find(cluster, "face_recognition", 1)
mv2.lock_till_released()
stage1 = ExecutionStageBuilder().with_model_variant(mv1, 100).build()
stage2 = ExecutionStageBuilder().with_model_variant(mv2, 100).build()
app = ApplicationBuilder(cluster, "face_recognition") \
    .with_stage(stage1) \
    .with_stage(stage2) \
    .build()
app.lock_while_starting()
```
