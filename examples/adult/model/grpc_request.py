import grpc
import hydro_serving_grpc as hs
import numpy as np
from grpc import ssl_channel_credentials

#            import hydro_serving_grpc as hs 

channel = grpc.secure_channel("dev.k8s.hydrosphere.io", credentials=ssl_channel_credentials())
stub = hs.PredictionServiceStub(channel)
model_spec = hs.ModelSpec(name="adult_test", signature_name="INFERRED_PIPELINE_SIGNATURE")
tensor_shape = hs.TensorShapeProto(dim=[hs.TensorShapeProto.Dim(size=-1), hs.TensorShapeProto.Dim(size=12)])
val = np.array([
    [
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1
    ]
], dtype="int64").flatten()
print(val.shape)
# val = val.flatten()

tensor = hs.TensorProto(dtype=hs.DT_INT64, tensor_shape=tensor_shape, float_val=val)
request = hs.PredictRequest(model_spec=model_spec, inputs={"input": tensor})
result = stub.Predict(request)
print(result)
