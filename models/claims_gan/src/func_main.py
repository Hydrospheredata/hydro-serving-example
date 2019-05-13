import hydro_serving_grpc as hs
import numpy as np
import tensorflow as tf
from keras.models import load_model


model = load_model("/model/files/gan.h5")
graph = tf.get_default_graph()


def gan(client_profile):
    with graph.as_default():
        data = tf.make_ndarray(client_profile)
        data = np.expand_dims(data, axis=0)
        result = model.predict(data)[0].tolist()

    answer_tensor_one = hs.TensorProto(
        double_val=[result[0]],
        dtype=hs.DT_DOUBLE)
    answer_tensor_two = hs.TensorProto(
        double_val=[result[1]],
        dtype=hs.DT_DOUBLE)

    return hs.PredictResponse(
        outputs={
            "class_one": answer_tensor_one,
            "class_two": answer_tensor_two
        }
    )
    
