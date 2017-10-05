import numpy as np
import tensorflow as tf


def convert_to_python(data):
    if isinstance(data, np.integer):
        return int(data)
    elif isinstance(data, np.floating):
        return float(data)
    elif isinstance(data, np.ndarray):
        return data.tolist()
    elif isinstance(data, np.matrix):
        return data.tolist()
    else:
        print("{0} isn't convertible to python".format(type(data)))
        return data


def convert_data_to_tensor_shape(data, shape: tf.TensorShape):
    if shape.ndims == 2:
        return np.matrix(data)
    elif shape.ndims > 2:
        return np.array(data)
    else:
        return data
