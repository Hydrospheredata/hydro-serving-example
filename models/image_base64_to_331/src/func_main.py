import tensorflow as tf;
from PIL import Image;
import io;
import base64;

import hydro_serving_grpc as hs;

def unpack(image_base64):

	encoded_image = image_base64.string_val[0];

	decoded_image = base64.b64decode(encoded_image);
	image = Image.open(io.BytesIO(decoded_image));

	resized_image = image.resize((331, 331));

	image_array = tf.keras.preprocessing.image.img_to_array(resized_image);

	image_shaped = image_array.reshape((1,) + image_array.shape);


	decoded_image_tensor_shape = hs.TensorShapeProto\
	(
		dim = \
		[
			hs.TensorShapeProto.Dim(size = dim)\
			for dim in image_shaped.shape
		]
	);

	decoded_image_tensor_proto = hs.TensorProto\
	(
		dtype = hs.DT_DOUBLE,
		double_val = image_shaped.flatten(),
		tensor_shape = decoded_image_tensor_shape
	);

	return hs.PredictResponse(outputs = {"shaped_image": decoded_image_tensor_proto});