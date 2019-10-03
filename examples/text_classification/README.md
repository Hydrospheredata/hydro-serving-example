# Amazon Review Sentiment Analysis
This demo shows how you can use Amazon dataset of customer reviews and ratings to train a model predicting whether review sentiment
 was positive or not.

To upload all models and instantiate applications from this demo 
```
dvc pull $(find . -type f -name "*.dvc")
hs apply
```

## Decsription
This model consists of two stages:
1. Text tokenization - tokenize string into an array of tokens with padding
    - [Model contract](models/tokenizer/serving.yaml) - contains deployment configuration
    - [Signature function](models/tokenizer/src/func_main.py) - entry point of model servable
    - [Tokenizer model](tokenizer.pickle) - tokenizer model (stored on s3).  You can pull it with `dvc pull models/tokenizer.pickle.dvc`

### Deployment
```commandline
hs upload --dir models/tokenizer
```

2. Sentiment prediction - classify array of tokens into two classes: 0 for negative, 1 for positive review. 
Prediction model is an LSTM model based on GloVe embeddings

    - [Model contract](models/estimator/serving.yaml) - contains deployment configuration
    - [Signature function](models/estimator/src/func_main.py) - entry point of model servable
    - [Pretrained amazon model](models/estimator/amazon_model.h5) - classification model (stored on s3). You can pull it with `dvc pull models/amazon_model.h5.dvc`


    To upload this stage separately to an HS cluster you can use `hs upload` command. 

### Deployment
```commandline
hs upload --dir models/estimator
```
