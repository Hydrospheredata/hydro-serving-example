# hydro-serving-example
This repo contains various demo scenarios and pre-trained models. Folder structure:








---------
## Demos

### object_detection
   SSD Tensorflow object detection serving data.
   
### random_cut_demo
   New model with Robust Random Cut Forest to detect anomalies.
   
### stateful_lstm_example
   Pipeline example with preprocessing, stateful LSTM and postprocessing

## Models
   To upload a model:
 ```bash
 pip install hs
 cd model/$MODEL_FOLDER
 hs cluster add --name <name> --server <server_addr>
 hs upload
 ```
  
   
