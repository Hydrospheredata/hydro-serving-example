import keras
import numpy as np
import tensorflow as tf
import hydro_serving_grpc as hs
from keras.models import load_model



# def extract_value(proto):
    # return np.array(proto.double_val)[0]
 

# 0. Load model once
model = load_model('/model/files/model.h5', compile=False)

global graph
graph = tf.get_default_graph() #this is a workaround of keras' issue with multithreading

def infer(**kwargs):
    # 1. Retrieve tensor's content and put it to numpy array
    tensor = kwargs["x"]
    data = np.array(tensor.double_val).reshape(1,300,3,3)
    # data = data.reshape(1, 2700)
    result = 0
    for i in range(data.shape[1]):
    # 2. Make a prediction
        with graph.as_default():
            vector = data[0,i,:,:].reshape(1,9)
            rec_vector= model.predict(vector)
            result += np.mean(np.square(vector - rec_vector), axis=0)

   # result = result/300
    # 3. Pack the answer
    # y_shape = hs.TensorShapeProto(dim=[hs.TensorShapeProto.Dim(size=1)])
    # y_shape = scalar
    y_tensor = hs.TensorProto(
        dtype=hs.DT_DOUBLE,
        double_val=result.flatten().tolist(),
        tensor_shape=hs.TensorShapeProto())

    # 4. Return the result
    return hs.PredictResponse(outputs={"value": y_tensor})

