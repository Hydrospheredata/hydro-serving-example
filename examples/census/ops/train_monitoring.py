import logging
import joblib
import pandas as pd
import numpy as np
from pyod.models.knn import KNN
from sklearn.model_selection import train_test_split

logging.basicConfig(format="%(asctime)-15s %(levelname)s %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


def load_data(filename="../data/adult.csv", **kwargs):
    logger.info("Loading data")

    df = pd.read_csv(filename, **kwargs).replace({'?': np.nan}).dropna()
    df.to_csv("../data/train.csv", index=False)
    return df


def load_transformers(filename="../models/model/encoders.joblib"):
    logger.info("Loading transformers")
    return joblib.load(filename)


def transform_data(data, transformers):
    logger.info("Transforming data")

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


def train_monitoring_model(data):
    logger.info("Training a monitoring model")

    X_train, X_test = train_test_split(np.array(data, dtype='float'), test_size=0.2)
    monitoring_model = KNN(contamination=0.05, n_neighbors=15, p=5)
    monitoring_model.fit(X_train)
    return monitoring_model


def dump_artifacts(model):
    logger.info("Dumping artifacts")

    joblib.dump(model, '../models/metric/model.joblib')


if __name__ == "__main__":
    transformers = load_transformers()
    df = load_data()
    df = transform_data(df, transformers)
    metric = train_monitoring_model(df)
    dump_artifacts(metric)
    
