import pandas as pd
import xgboost as xgb
import pickle
import hydro_serving_grpc as hs

gbm = pickle.load(open("/model/files/trained.model", "rb"))

def infer(**kwargs):
    df = pd.DataFrame({'Pclass': kwargs['pclass'].int_val, 'Sex': kwargs['sex'].string_val, 'Age': kwargs['age'].int_val, 'Fare': kwargs['fare'].double_val, 'Parch': kwargs['parch'].int_val})
    df['Sex'] = df['Sex'].map({'male':0,'female':1}).to_frame()
    score = gbm.predict(df.values)
    return hs.PredictResponse(outputs={"survived": hs.TensorProto(
        dtype=hs.DT_INT32,
        int_val=score,
        tensor_shape=hs.TensorShapeProto(
            dim=[hs.TensorShapeProto.Dim(size=-1)]
        )
    )})

