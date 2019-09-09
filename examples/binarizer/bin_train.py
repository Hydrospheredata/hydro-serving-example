from pyspark.ml import Pipeline
from pyspark.sql import SparkSession
from pyspark.ml.feature import Binarizer

if __name__ == "__main__":
    spark = SparkSession\
        .builder\
        .appName("BinarizerExample")\
        .getOrCreate()

    continuousDataFrame = spark.createDataFrame([(4)], [ "feature"])
    binarizer = Binarizer(threshold=5, inputCol="feature", outputCol="binarized_feature")
    pipeline = Pipeline(stages=[binarizer])
    pipeline = pipeline.fit(continuousDataFrame)
    pipeline.write().overwrite().save("binarizer")