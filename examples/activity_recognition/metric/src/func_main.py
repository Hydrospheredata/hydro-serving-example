import keras
import numpy as np
import tensorflow as tf
from keras.models import load_model

model = load_model('/model/files/model.h5', compile=False)
graph = tf.get_default_graph() # this is a workaround of keras' issue with multithreading


def infer(x, y):
    with graph.as_default():
        score = 0
        for i in range(x.shape[1]):
            vector = x[0,i,:,:].reshape(1,9)
            rec_vector = model.predict(vector)
            score += np.mean(np.square(vector - rec_vector), axis=1).item()
        return {"value": score}
