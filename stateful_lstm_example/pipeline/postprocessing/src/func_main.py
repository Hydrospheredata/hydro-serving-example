import hydro_serving_grpc as hs


def detect(result):
    print(result)
    vals = result.double_val

    is_anomaly = False
    for val in vals:
        if val < 0.05:
            is_anomaly = True

    anomaly = hs.TensorProto(
        dtype=hs.DT_BOOL,
        bool_val=[is_anomaly]
    )

    print(result)
    print(anomaly)
    return hs.PredictResponse(
        outputs={
            "result": result,
            "anomaly": anomaly
        }
    )
