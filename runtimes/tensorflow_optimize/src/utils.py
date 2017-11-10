import tensorflow as tf
import numpy as np
from tensorflow.python.saved_model.signature_constants import DEFAULT_SERVING_SIGNATURE_DEF_KEY
from tensorflow.python.tools.optimize_for_inference_lib import optimize_for_inference

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

def load_and_optimize(model_path):
    with tf.Session() as temp_sess:
        meta_graph = tf.saved_model.loader.load(temp_sess, [tf.saved_model.tag_constants.SERVING], model_path)
        print("Model loaded.")
        signature = meta_graph.signature_def[DEFAULT_SERVING_SIGNATURE_DEF_KEY]
        input_types = list([x.dtype for x in signature.inputs.values()])
        inputs = list(signature.inputs.keys())
        outputs = list(signature.outputs.keys())
        old_input_tensors = {x: temp_sess.graph.get_tensor_by_name(signature.inputs[x].name) for x in inputs}
        old_output_tensors = {x: temp_sess.graph.get_tensor_by_name(signature.outputs[x].name) for x in outputs}
        print("Input tensors:")
        [print(x) for x in inputs]
        print("Output tensors:")
        [print(x) for x in outputs]

        print("Optimizing TensorFlow model...")
        preoptimized = tf.graph_util.convert_variables_to_constants(
            temp_sess,
            temp_sess.graph_def,
            list(map(lambda x: x.name.split(':')[0], old_output_tensors.values()))
        )
        optimized = optimize_for_inference(
            preoptimized,
            list(map(lambda x: x.name.split(':')[0], old_input_tensors.values())),
            list(map(lambda x: x.name.split(':')[0], old_output_tensors.values())),
            input_types)

        with tf.Graph().as_default() as g:
            tf.import_graph_def(optimized, name="")
            opt_sess = tf.Session(graph = g)
            tf.import_graph_def(optimized, name="")
            print("Getting new input tensors...")
            input_tensors = {x: opt_sess.graph.get_tensor_by_name(signature.inputs[x].name) for x in inputs}
            output_tensors = {x: opt_sess.graph.get_tensor_by_name(signature.outputs[x].name) for x in outputs}
            # restore shape information for tensors
            for i in inputs:
                input_tensors[i].set_shape(old_input_tensors[i].shape)
            for i in outputs:
                output_tensors[i].set_shape(old_output_tensors[i].shape)
            return opt_sess, input_tensors, output_tensors
