## Stateful LSTM pipeline demo

Pipeline consists of 3 steps:
1. Stateless [preprocessing](/stateful_lstm_example/pipeline/preprocessing)
2. Stateful [LSTM](/stateful_lstm_example/pipeline/lstm)
3. Stateless [postprocessing](/stateful_lstm_example/pipeline/postprocessing)


Post- and pre-processing are implemented as Python functions.
Stateful LSTM is implemented in Tensorflow, and exported by our custom SavedModelBuilder with state support.


## How to use:
1. Prepare LSTM
    1. Train: run training [script](/stateful_lstm_example/pipeline/lstm/training/src/training.py)
    2. Export: run export [script](/stateful_lstm_example/pipeline/lstm/training/src/export.py).
    Export script stores additional information in collections:
     - `h_zero_states` collection contains tensors with zero state.
     - `h_state_placeholders` collection contains state placeholders for fetching.  
     i-th `zero_state` tensor must be compatible with i-th `state_placeholder`.
2. Run `hydro-serving` from docker-compose
3. Upload all stages: 
    NOTICE: there are optional parameters HOST and PORT for `hs upload`.
You might want to change them if you have different infrastructure.
    1. `cd pipeline/preprocessing && hs upload`
    2. `cd pipeline/lstm && hs upload`
    3. `cd pipeline/postprocessing && hs upload`
4. Run demo Jupyter [Notebook](/stateful_lstm_example/demo.ipynb)

## How to export stateful Tensorflow model 
We developed a custom `SavedModelBuilder` compatible with Tensorflow `SavedModel` message.
The main difference is that we store zerostate tensors in `h_zero_states` collection, and
state placeholders in `h_state_placeholders` collection.

```python
# Add zero state tensors
sess.graph.add_to_collection("h_zero_states", rnn_init_state[0].c)
sess.graph.add_to_collection("h_zero_states", rnn_init_state[0].h)

# Add state placeholders
sess.graph.add_to_collection("h_state_placeholders", rnn_final_state[0].c)
sess.graph.add_to_collection("h_state_placeholders", rnn_final_state[0].h)

builder = StatefulSavedModelBuilder("/tmp/model") # note the usage of StatefulSavedModelBuilder
inference_signature = (
    tf.saved_model.signature_def_utils.build_signature_def(...)
)

builder.add_meta_graph_and_variables(
    sess, [tag_constants.SERVING],
    signature_def_map={
        'infer': inference_signature,
    }
)
builder.save()

```
