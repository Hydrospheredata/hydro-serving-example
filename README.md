# Hydrosphere examples

This repo contains demo scenarios and pre-trained models to show Hydrosphere capabilities.

## Data and artifacts management

Some models contain dataset or artifacts for training and testing purposes. Those artifacts are managed by [dvc](https://github.com/iterative/dvc). 

To load data follow below steps.
- Install `dvc` package.
   ```sh
   pip install dvc
   ```
- Pull all or necessary data from the remote storage.
   ```sh
   dvc pull examples/adult/data/adult.csv.dvc # load specific file
   dvc pull # load all remote files
   ``` 

## Python examples

To learn more, how to deploy a python model, check out our [getting started](https://docs.hydrosphere.io/quickstart/getting-started) guide.

* [Simple models](examples/simple_models)
   * [Hand-written digit classification model](examples/simple_models/mnist_py)
   * [Fraud detection model](examples/simple_models/fraud_detection)
   * [Object detection model based on MobileNet](examples/simple_models/mobilenet)
   * [Titanic survival classification model](examples/simple_models/titanic_xgboost)
* [Pipelines](examples/pipelines)
   * [Face recognition pipeline based on FaceNet](examples/pipelines/face_recognition)
   * [Amazon reviews sentiment classification model](examples/pipelines/text_classification)
* [Custom metrics](examples/custom_metrics)
   * [Census classification model](examples/custom_metrics/census)
