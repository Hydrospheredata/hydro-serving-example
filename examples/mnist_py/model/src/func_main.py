import numpy as np
import tensorflow as tf
from keras.models import load_model

model = load_model("/model/files/model.h5", compile=False)
graph = tf.get_default_graph()

def predict(images):
    with graph.as_default():
        probas = model.predict(images.reshape((-1, 28 * 28)))

    return {
        "classes": np.array(probas).argmax(axis=0),
        "probabilities": probas.astype('double')
    }
