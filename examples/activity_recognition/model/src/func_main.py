import numpy as np
import tensorflow as tf
from keras.models import load_model


model = load_model('/model/files/model.h5')
graph = tf.get_default_graph() # this is a workaround of keras' issue with multithreading


def infer(x):
    with graph.as_default():
        return {"y": model.predict(x)}