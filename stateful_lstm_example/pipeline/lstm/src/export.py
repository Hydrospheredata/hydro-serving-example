import tensorflow as tf
import os
import shutil
import model_def

export_dir = "../models"

if not os.path.exists(export_dir):
    os.mkdir(export_dir)

export_sess = tf.Session()
seq_length = 1
batch_size = 1
data_dim = 24
dropout_kp = 0.5
num_labels = 4

x, y, rnn, rnn_init_state, rnn_final_state, logits, loss, dropout_keep_prob = model_def.model(
    seq_length=seq_length, batch_size=batch_size
)

# Create a saver for all variables
tf_vars_to_save = tf.trainable_variables()
saver = tf.train.Saver(tf_vars_to_save)

export_sess.run(tf.global_variables_initializer())

# Loading checkpoint file from disk
latest_checkpoint = tf.train.latest_checkpoint("./checkpoints/")
saver.restore(export_sess, latest_checkpoint)

# Add state tensors to collection
export_sess.graph.add_to_collection("h_zero_states", rnn_init_state[0].c)
export_sess.graph.add_to_collection("h_zero_states", rnn_init_state[0].h)

export_sess.graph.add_to_collection("h_state_placeholders", rnn_final_state[0].c)
export_sess.graph.add_to_collection("h_state_placeholders", rnn_final_state[0].h)

versions = [int(x) for x in filter(lambda x: os.path.isdir(os.path.join(export_dir, x)), os.listdir(export_dir))]
print(versions)
if len(versions) != 0:
    latest_version = max(versions)
    current_version = str(latest_version + 1)
else:
    current_version = "1"

export_path = os.path.join(export_dir, current_version)
builder = tf.saved_model.builder.SavedModelBuilder(export_path)
print("Exporting to {}".format(export_path))
legacy_init_op = tf.group(tf.tables_initializer(), name='legacy_init_op')

inference_signature = (
    tf.saved_model.signature_def_utils.build_signature_def(
        inputs={'data': tf.saved_model.utils.build_tensor_info(x)},
        outputs={'result': tf.saved_model.utils.build_tensor_info(logits)},
        method_name='infer'))

builder.add_meta_graph_and_variables(
    export_sess, [tf.saved_model.tag_constants.SERVING],
    signature_def_map={
        'infer':
            inference_signature,
    })
builder.save()

print("Training done.")
