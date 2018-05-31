# Model zoo

This directory contains pre-trained models from various ML libraries.

## How to use

```bash
cd $MODEL_OF_YOUR_CHOICE
hs upload --host $HOST --port $PORT
```

Now, your model is uploaded to the `hydro-serving` and you can create applications.

### Spark models

* binarizer 
* randomforest_classifier
* word2vec

### Tensorflow models

* stateful_lstm
* autoencoder

### Python scripts

* stateful_lstm_postprocessing
* stateful_lstm_preprocessing	
* claims_model
