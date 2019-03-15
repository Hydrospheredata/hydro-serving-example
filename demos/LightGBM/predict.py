from datetime import datetime;
import pandas as pd;
import numpy as np;
from sklearn.externals import joblib;
import json;

def getDataFrame(filename):
    """
Returns pandas DataFrame built upon data stored as lines of jsons in a file
(1 line - 1 json)
"""
    json_file = open(filename, "r");

    samples_list = []

    for sample_json in json_file:
        sample_dict = json.loads(sample_json);
        samples_list.append(sample_dict);

    data_frame = pd.DataFrame.from_dict(samples_list);

    return data_frame;


def main():

    logfile = open("predict.log", "a+");

    def writeLog(note):
        print(note);
        logfile.write("{}\r\n".format(note));

    writeLog("Log Start: {}".format(datetime.now()));

    writeLog("Reading samples...");

    try:
        sample_set = getDataFrame("samples.json");
        writeLog("Samples read, data frame built successfully.");
    except Exception as exception:
        writeLog("{}".format(exception));

    writeLog("Loading the model...");
    
    try:    
        model = joblib.load("model/forecaster.pkl"); #it is a pretrained LightGBM model.
        writeLog("Model loaded successfully...");
    except Exception as exception:
        writeLog("{}".format(exception));

    writeLog("Making prediction...");

    try:
        prediction = model.predict(sample_set);
        writeLog("Prediction made:");
        writeLog("----------------------------");
        writeLog(repr(prediction));
        writeLog("Prediction __class__: {}".format(prediction.__class__))
    except Exception as exception:
        writeLog("{}".format(exception));

    writeLog("Done.");
    writeLog("----------------------------");

    logfile.close();

    return prediction;

if __name__ == "__main__":
    main();