import keras
import numpy as np
import tensorflow as tf
import hydro_serving_grpc as hs
from keras.models import load_model

model = load_model('/model/files/model.h5', compile=False)

global graph
graph = tf.get_default_graph() #this is a workaround of keras' issue with multithreading
def infer(**kwargs):

    tensor = kwargs["x"]
    data = np.array(tensor.double_val).reshape(1,300,3,3)
    result = 0
    for i in range(data.shape[1]):
        with graph.as_default():
            vector = data[0,i,:,:].reshape(1,9)
            rec_vector= model.predict(vector)
            result += np.mean(np.square(vector - rec_vector), axis=0)
    y_tensor = hs.TensorProto(
        dtype=hs.DT_DOUBLE,
        double_val=result.flatten().tolist(),
        tensor_shape=hs.TensorShapeProto())

    # 4. Return the result
    return hs.PredictResponse(outputs={"value": y_tensor})

