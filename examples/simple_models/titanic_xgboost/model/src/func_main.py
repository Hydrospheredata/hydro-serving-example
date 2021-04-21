import pickle
import pandas as pd

gbm = pickle.load(open("/model/files/trained.model", "rb"))


def infer(pclass, sex, age, fare, parch):
    df = pd.DataFrame({
        'Pclass': pclass, 
        'Sex': sex, 
        'Age': age, 
        'Fare': fare, 
        'Parch': parch
    }, index=[0])
    df['Sex'] = df['Sex'].map({'male': 0, 'female': 1}).to_frame()
    score = gbm.predict(df.values)
    return {"survived": score.item()}
