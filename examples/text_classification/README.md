# Amazon review sentiment analysis
This model consists of two stages:
1. text tokenization - detecting faces in img
2. text classification - 0 for negative, 1 for positive review


## Text tokenization: 
- [Model contract](models/tokenizer/serving.yaml) - contains deployment configuration
- [Signature function](models/tokenizer/src/func_main.py) - entry point of model servable
- [Tokenizer model](models/tokenizer.pickle) - tokenizer model (stored on s3)

### Load model

Models for amazon review are stored on s3 bucket as they are too large. To download them you have to configure dvc (see [guide](../../README.md))

Then you can easily pull model:
```commandline
dvc pull models/tokenizer.pickle.dvc
```

### Deployment
```commandline
cd models/tokenizer
hs upload
```

## Classification:
- [Model contract](models/estimator/serving.yaml) - contains deployment configuration
- [Signature function](models/estimator/src/func_main.py) - entry point of model servable
- [Pretrained amazon model](models/estimator/amazon_model.h5) (stored on s3)

### Load model 
```commandline
dvc pull models/estimator/amazon_model.h5.dvc
```

### Deployment
```commandline
cd models/estimator
hs upload
```
