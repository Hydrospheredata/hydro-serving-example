import pickle

import hydro_serving_grpc as hs
import pandas as pd

gbm = pickle.load(open("/model/files/trained.model", "rb"))


def infer(pclass, sex, age, fare, parch):
    df = pd.DataFrame({'Pclass': pclass.int_val, 'Sex': sex.string_val, 'Age': age.int_val, 'Fare': fare.double_val,
                       'Parch': parch.int_val})
    df['Sex'] = df['Sex'].map({'male': 0, 'female': 1}).to_frame()
    score = gbm.predict(df.values)
    tensor = hs.TensorProto(
        dtype=hs.DT_INT32,
        int_val=score,
        tensor_shape=hs.TensorShapeProto(
            dim=[hs.TensorShapeProto.Dim(size=-1)]
        )
    )
    return hs.PredictResponse(outputs={"survived": tensor})
