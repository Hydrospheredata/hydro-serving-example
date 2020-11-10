import logging

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


logging.basicConfig(format="%(asctime)-15s %(levelname)s %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


def load_data(filename="../data/adult.csv", **kwargs):
    logger.info("Loading data")

    df = pd.read_csv(filename, **kwargs).replace({'?': np.nan}).dropna()
    df.to_csv("../data/train.csv", index=False)
    return df


def train_encoder(data): 
    logger.info("Training encoder")

    categorical_features = [
        "workclass", "education", "marital-status",
        "occupation", "relationship", "race", "gender",
        "capital-gain", "capital-loss", "native-country", "income"
    ]
    numerical_features = [
        "age", "fnlwgt", "educational-num",
        "capital-gain", "capital-loss", "hours-per-week"
    ]
        
    encoders = {}
    for column in categorical_features:
        categorical_encoder = LabelEncoder()
        data[column] = categorical_encoder.fit_transform(data[column])
        encoders[column] = categorical_encoder
    return encoders


def train_model(data):
    logger.info("Training model")

    X, y = data.drop('income', axis=1), data['income']
    train_X, test_X, train_y, test_y = train_test_split(
        X, y.astype(int), stratify=y, test_size=0.2, random_state=42)

    clf = RandomForestClassifier(
        n_estimators=20, 
        max_depth=10,
        n_jobs=5,
        random_state=42
    ).fit(train_X, train_y)
    return clf
    

def dump_artifacts(model, encoder):
    logger.info("Dumping artifacts")

    joblib.dump(model, '../model/model.joblib')
    joblib.dump(encoder, "../model/encoders.joblib")


if __name__ == "__main__": 
    data = load_data()
    encoder = train_encoder(data)
    model = train_model(data)
    dump_artifacts(model, encoder)
