import grpc 
import numpy as np
import hydro_serving_grpc as hs
from grpc import ssl_channel_credentials
# connect to your ML Lamba instance
channel = grpc.secure_channel("dev.k8s.hydrosphere.io", credentials=ssl_channel_credentials())

stub = hs.PredictionServiceStub(channel)

# 1. define a model, that you'll use
model_spec = hs.ModelSpec(name="activity_recognition", signature_name="infer")
# 2. define tensor_shape for Tensor instance
tensor_shape = hs.TensorShapeProto(dim=[hs.TensorShapeProto.Dim(size=1), hs.TensorShapeProto.Dim(size=300),hs.TensorShapeProto.Dim(size=3),hs.TensorShapeProto.Dim(size=3)])
# 3. define tensor with needed data
val = np.load('test.npy').astype(np.float32)
val = val.flatten()
tensor = hs.TensorProto(dtype=hs.DT_DOUBLE, tensor_shape=tensor_shape, double_val=val)
# 4. create PredictRequest instance
request = hs.PredictRequest(model_spec=model_spec, inputs={"x": tensor})

# call Predict method
#exec(open("grpc_test2.py").read())
result = stub.Predict(request)
print(result)
