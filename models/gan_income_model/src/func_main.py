import hydro_serving_grpc as hs
import numpy as np
from keras.models import load_model

model = load_model("/model/files/gan.h5")

def gan(client_profile):
    data = client_profile.double_val

    print(data)
    print(np.array([data]))
    print("KEK")

    # gan_prediction = model.predict(np.array([np.array(data)]))
    # res = np.argmax(gan_prediction)

    # gan_res = list(map(lambda x: np.argmax(x), model.predict(np.array([data]))))

    res = model.predict(np.array([data]))[0].tolist()

    # answer_tensor = hs.TensorProto(
    #     double_val=[res],
    #     dtype=hs.DT_DOUBLE
    # )

    # return hs.PredictResponse(
    #     outputs={
    #         "result": answer_tensor
    #     }
    # )

    class_one = res[0]
    class_two = res[1]

    answer_tensor_one = hs.TensorProto(
        double_val=[class_one],
        dtype=hs.DT_DOUBLE
    )
    answer_tensor_two = hs.TensorProto(
        double_val=[class_two],
        dtype=hs.DT_DOUBLE
    )

    return hs.PredictResponse(
        outputs={
            "class_one": answer_tensor_one,
            "class_two": answer_tensor_two
        }
    )
    
