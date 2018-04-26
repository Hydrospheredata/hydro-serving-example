import hydro_serving_grpc as hs


def normalize(data):
    max_val = max(data.double_val)
    norm_data = [float(x) / max_val for x in data.double_val]

    return {
        "data": hs.TensorProto(
            dtype=hs.DT_DOUBLE,
            double_val=norm_data,
            shape=data.shape
        )
    }
