import numpy as np
import tensorflow as tf
import hydro_serving_grpc as hs
from keras.models import load_model

# prepare the graph to load model into
graph = tf.get_default_graph()

# load model and compile it for evaluation step
autoencoder = load_model("/model/files/relu-2layers-4units.3.h5")
autoencoder.compile(loss='mse', optimizer='adam')


def infer(**kwargs):
    # use graph with initialized model in it
    with graph.as_default():

        features = kwargs['X']
        data = np.array(features.double_val) \
            .reshape([dim.size for dim in features.tensor_shape.dim])
        predicted = autoencoder.predict(data)
        score = np.mean(np.square(predicted - data), axis=1)
        
        response_shape = hs.TensorShapeProto(
            dim=[hs.TensorShapeProto.Dim(size=item) for item in (1, 1)])
        response_tensor = hs.TensorProto(
            dtype=hs.DT_DOUBLE,
            double_val=np.expand_dims(score.flatten(), axis=0),
            tensor_shape=response_shape)

        return hs.PredictResponse(outputs={"reconstructed": response_tensor})