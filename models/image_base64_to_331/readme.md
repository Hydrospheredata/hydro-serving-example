Model proved to be workable and servable in **hydrosphere.io** environment ver. **2.0.1**

Preprocessing base64 encoded image into tensor of shape [1, 331, 331, 3].

This is an example of image preprocessing model for passing base64 encoded image further to Keras, TensorFlow or any other model expecting tensor of shape [1, height, width, 3] to inference.

Particularly this model resizes an image to 331x331 dimensions (e.g. for NASNetLarge inputs).
The size is defineed in `resized_image = image.resize((331, 331))` code line, and don't froget to change output shape in serving.yaml accordingly.
