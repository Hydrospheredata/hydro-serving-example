from keras.models import load_model
import hydro_serving_grpc as hs
import tensorflow as tf
import numpy as np
amazon_model = load_model('/model/files/amazon_model.h5')
amazon_model._make_predict_function()
graph = tf.get_default_graph()
def predict(tokenized):
    global graph
    tokenized_sentence = tokenized.int64_val
    tokenized_sentence = np.array([tokenized_sentence])
    with graph.as_default():
        prediction = amazon_model.predict([tokenized_sentence])
    confidence = prediction[0,0]
    label = 1 if confidence >= 0.5 else 0
    conf_tensor = hs.TensorProto(
        double_val=[confidence],
        dtype=hs.DT_DOUBLE,
        tensor_shape=hs.TensorShapeProto())

    label_tensor = hs.TensorProto(
        int_val=[label],
        dtype=hs.DT_INT32,
        tensor_shape=hs.TensorShapeProto())

    return hs.PredictResponse(outputs={'confidence': conf_tensor, 'label':label_tensor})

