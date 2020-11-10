import numpy as np
import tensorflow as tf
from keras.applications import mobilenet_v2

mobile_net = mobilenet_v2.MobileNetV2(
    alpha=0.35,
    weights="/model/files/mobilenet_v2_weights_tf_dim_ordering_tf_kernels_0.35_224"
)
graph = tf.get_default_graph()


def predict(input):
    images = mobilenet_v2.preprocess_input(input)
    with graph.as_default():
        probas = mobile_net.predict(images)
        classes = probas.argmax(axis=1)
        
    return {
        "classes": classes.astype("int64"),
        "probabilities": probas.astype("double")
    }
