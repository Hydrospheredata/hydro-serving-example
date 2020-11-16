import numpy as np
import pandas as pd
from joblib import load

monitoring_model = load('/model/files/model.joblib')
encoders = load('/model/files/encoders.joblib')


def transform_data(data, transformers):
    categorical_features = [
        "workclass", "education", "marital-status",
        "occupation", "relationship", "race", "gender",
        "capital-gain", "capital-loss", "native-country", "income"
    ]
    numerical_features = [
        "age", "fnlwgt", "educational-num",
        "capital-gain", "capital-loss", "hours-per-week"
    ]

    for column in categorical_features:
        data[column] = transformers[column].fit_transform(data[column])
    return data


def predict(**kwargs):
    x = pd.DataFrame.from_dict({'input': kwargs}, orient='index')
    X = transform_data(x, encoders)
    value = monitoring_model.decision_function(X)
    return {"value": value.astype("double").item()}
