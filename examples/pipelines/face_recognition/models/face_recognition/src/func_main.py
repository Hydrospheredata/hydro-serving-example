import os
import pickle

import numpy as np
import tensorflow as tf
from tensorflow.python.platform import gfile

facenet_path = '/model/files/20180402-114759.pb'
classifier_path = '/model/files/lfw_classifier.pkl'


def prewhiten(x):
    mean = np.mean(x)
    std = np.std(x)
    std_adj = np.maximum(std, 1.0 / np.sqrt(x.size))
    y = np.multiply(np.subtract(x, mean), 1 / std_adj).astype(np.float32)
    return y


def load_facenet_model(pth, input_map=None):
    facenet_exp = os.path.expanduser(facenet_path)
    if os.path.isfile(facenet_exp):
        with gfile.FastGFile(facenet_exp, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            tf.import_graph_def(graph_def, input_map=input_map, name='')


def load_classifier(pth):
    classifier_filename_exp = os.path.expanduser(pth)
    with open(classifier_filename_exp, 'rb') as infile:
        (model, class_names) = pickle.load(infile)
        return model, class_names


classifier, class_names = load_classifier(classifier_path)

# loading facenet model
graph = tf.Graph()
with graph.as_default():
    with tf.Session(graph=graph) as sess:
        load_facenet_model(facenet_path)
        images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
        embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
        phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")


def infer(faces):
    # preprocess imgs for facenet
    for i in range(len(faces)):
        faces[i] = prewhiten(faces[i])

    with graph.as_default():
        with tf.Session(graph=graph) as sess:
            feed_dict = {images_placeholder: faces, phase_train_placeholder: False}
            emb_array = sess.run(embeddings, feed_dict=feed_dict)
            predictions = classifier.predict_proba(emb_array)
            class_indices = np.argmax(predictions, axis=1)
            classes = [class_names[index] for index in class_indices]
            return {"y": np.array(classes).astype("str")}
