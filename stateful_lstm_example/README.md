## Stateful LSTM pipeline demo

Pipeline consists of 3 steps:
1. Stateless [preprocessing](stateful_lstm_example/pipeline/preprocessing)
2. Stateful [LSTM](stateful_lstm_example/pipeline/lstm)
3. Stateless [postprocessing](stateful_lstm_example/pipeline/postprocessing)


Post- and pre-processing are implemented as Python functions.
Stateful LSTM is implemented in Tensorflow, and exported by our custom SavedModelBuilder with state support.


## How to use:
1. Prepare LSTM
    1. Train: run training [script](stateful_lstm_example/pipeline/lstm/training/src/training.py)
    2. Export: run export [script](stateful_lstm_example/pipeline/lstm/training/src/export.py).
    Export script stores additional information in collections:
     - `h_zero_states` collection contains tensors with zero state.
     - `h_state_placeholders` collection contains state placeholders for fetching.  
     i-th `zero_state` tensor must be compatible with i-th `state_placeholder`.
2. Run `hydro-serving` from docker-compose
3. Upload all stages: `make upload-all`. NOTICE: there are optional parameters HOST and PORT.
You might want to change them if you have different infrastructure.
4. Run demo Jupyter [Notebook](stateful_lstm_example/demo.ipynb)
