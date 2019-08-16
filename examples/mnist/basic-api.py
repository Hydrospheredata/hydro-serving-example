import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

learning_rate = 0.01
n_epochs = 30
batch_size = 32
training_size = 10000
test_size = 10000
export_dir = './servables/mnist_linear'


# Prepare data
mnist = input_data.read_data_sets("./data/mnist")

train_img, train_lbl = mnist.train.images, mnist.train.labels
test_img, test_lbl = mnist.test.images, mnist.test.labels
val_img, val_lbl = mnist.validation.images, mnist.validation.labels

train = (train_img, tf.one_hot(train_lbl, 10))
test = (test_img, tf.one_hot(test_lbl, 10))
val = (val_img, tf.one_hot(val_lbl, 10))

train_data = tf.data.Dataset.from_tensor_slices(train).shuffle(training_size).batch(batch_size)
test_data = tf.data.Dataset.from_tensor_slices(test).shuffle(test_size).batch(batch_size)

print(train_data.output_types, train_data.output_shapes)
iterator = tf.data.Iterator.from_structure(
    train_data.output_types, train_data.output_shapes)
img, label = iterator.get_next()

train_init = iterator.make_initializer(train_data)	# initializer for train_data
test_init = iterator.make_initializer(test_data)	# initializer for test_data

# Define model 
weights = tf.get_variable("weight", shape=[784, 10], initializer=tf.truncated_normal_initializer(stddev=0.01))
bias = tf.get_variable("bias", shape=[10], initializer=tf.zeros_initializer)

normed = tf.nn.l2_normalize(img)
logits = tf.matmul(normed, weights) + bias
pred = tf.nn.softmax(logits)

# Define loss
entropy = tf.nn.softmax_cross_entropy_with_logits_v2(
    logits=logits, labels=tf.stop_gradient(label))
loss = tf.reduce_mean(entropy)

# Define optimizer
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(loss)

# Define evaluation ops
correct_preds = tf.equal(tf.argmax(pred, 1), tf.argmax(label, 1))
accuracy = tf.reduce_sum(tf.cast(correct_preds, tf.float32))


sess = tf.Session()
sess.run(tf.global_variables_initializer())

# Run training 
for i in range(n_epochs): 	
    sess.run(train_init)
    total_loss, n_batches = 0, 0
    try:
        while True:
            _, l = sess.run([optimizer, loss])
            total_loss += l
            n_batches += 1
    except tf.errors.OutOfRangeError:
        pass
    print('Average loss epoch {0}: {1}'.format(i, total_loss/n_batches))

# Run evaluation
sess.run(test_init)
total_correct_preds = 0
try:
    while True:
        accuracy_batch = sess.run(accuracy)
        total_correct_preds += accuracy_batch
except tf.errors.OutOfRangeError:
    pass
print('Accuracy {0}'.format(total_correct_preds/test_size))

# Save model
signature_map = {
    "infer": tf.saved_model.signature_def_utils.predict_signature_def(
        inputs={"img": img}, outputs={"pred": pred})
}

builder = tf.saved_model.builder.SavedModelBuilder(export_dir)
builder.add_meta_graph_and_variables(
    sess=sess, 
    tags=[tf.saved_model.tag_constants.SERVING],
    signature_def_map=signature_map)
builder.save()