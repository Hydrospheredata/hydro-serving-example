import hydro_serving_grpc as hs

def claim(client_profile):
    data = client_profile.double_val

    answer_tensor = hs.TensorProto(
        double_val=[sum(data)*10],
        dtype=hs.DT_DOUBLE
    )

    return hs.PredictResponse(
        outputs={
            "amount": answer_tensor
        }
    )
    
