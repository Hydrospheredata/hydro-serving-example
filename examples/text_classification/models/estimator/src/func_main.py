from keras.models import load_model
import tensorflow as tf
import numpy as np

amazon_model = load_model('/model/files/amazon_model.h5')
amazon_model._make_predict_function()
graph = tf.get_default_graph()


def predict(tokenized):
    with graph.as_default():
        prediction = amazon_model.predict([tokenized.reshape(1, 100)])

    confidence = prediction[0,0].astype('double')
    return {
        "confidence": confidence,
        "label": np.array([1 if confidence >= 0.5 else 0]).item()
    }
