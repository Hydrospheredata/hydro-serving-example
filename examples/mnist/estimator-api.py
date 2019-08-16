import numpy as np
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

def input_fn(path="data/mnist", data="train", batch_size=256):
    mnist = input_data.read_data_sets("data/mnist")
    data_imgs = getattr(mnist, data).images
    data_labels = getattr(mnist, data).labels.astype(np.int32)
    data_tuple = (data_imgs, data_labels)

    dataset = (tf.data.Dataset
        .from_tensor_slices(data_tuple)
        .batch(batch_size))
    iterator = dataset.make_one_shot_iterator()
    imgs, labels = iterator.get_next()
    return {"imgs": imgs}, labels

tf.logging.set_verbosity(tf.logging.DEBUG)
imgs = tf.feature_column.numeric_column("imgs", shape=(784,))
estimator = tf.estimator.DNNClassifier(
    hidden_units=[256, 64],
    feature_columns=[imgs],
    n_classes=10,
    model_dir='./models/mnist')

train_spec = tf.estimator.TrainSpec(
    input_fn=lambda: input_fn(data="train"), max_steps=10000)
eval_spec = tf.estimator.EvalSpec(
    input_fn=lambda: input_fn(data="test"))
tf.estimator.train_and_evaluate(estimator, train_spec, eval_spec)

serving_input_receiver_fn = tf.estimator.export.build_raw_serving_input_receiver_fn({
    "imgs": tf.placeholder(tf.float32, shape=(None, 784))})
estimator.export_savedmodel("./servables/mnist_dnn", serving_input_receiver_fn)