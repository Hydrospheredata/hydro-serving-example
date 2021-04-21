import pickle

import numpy as np
import pandas as pd
import xgboost as xgb

from sklearn.base import TransformerMixin


def age_converter(text):
    try:
        return int(text.rstrip())
    except ValueError:
        return np.nan


def load_data(path): 
    df = pd.read_csv(path)
    df.columns = df.columns.str.rstrip()
    df["Age"] = df["Age"].apply(age_converter)
    return df


train_df = load_data("../data/train.csv")
test_df = load_data("../data/test.csv")


class DataFrameImputer(TransformerMixin):
    def fit(self, X, y=None):
        self.fill = pd.Series([X[c].value_counts().index[0]
                               if X[c].dtype == np.dtype('O') else X[c].median() for c in X],
                              index=X.columns)
        return self

    def transform(self, X, y=None):
        return X.fillna(self.fill)


feature_columns_to_use = ['Pclass', 'Sex', 'Age', 'Fare', 'Parch']
nonnumeric_columns = ['Sex']

big_X = train_df[feature_columns_to_use].append(test_df[feature_columns_to_use])
big_X_imputed = DataFrameImputer().fit_transform(big_X)

big_X_imputed['Sex'] = big_X_imputed['Sex'].map({'male': 0, 'female': 1}).to_frame()
train_X = big_X_imputed[0:train_df.shape[0]].values
test_X = big_X_imputed[train_df.shape[0]::].values
train_y = train_df['Survived']

gbm = xgb.XGBClassifier(max_depth=3, n_estimators=300, learning_rate=0.05).fit(train_X, train_y)

pickle.dump(gbm, open("../model/trained.model", "wb"))
