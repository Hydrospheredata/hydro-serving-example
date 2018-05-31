import hydro_serving_grpc as hs


def normalize(data):
    print(data)
    max_val = max(data.double_val)
    norm_data = [float(x) / max_val for x in data.double_val]
    shape = hs.TensorShapeProto(dim=[
        hs.TensorShapeProto.Dim(size=1),
        hs.TensorShapeProto.Dim(size=1),
        hs.TensorShapeProto.Dim(size=24)
    ])
    data = hs.TensorProto(
        dtype=hs.DT_DOUBLE,
        double_val=norm_data,
        tensor_shape=shape
    )
    print(data)
    return hs.PredictResponse(
        outputs={
            "data": data
        }
    )
