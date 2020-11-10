import numpy as np
from sklearn.externals import joblib

clf = joblib.load('/model/files/rf.joblib.pkl')


def infer(features):
    prediction = clf.predict(features)
    return {"is_fraud": prediction.astype('bool')}
