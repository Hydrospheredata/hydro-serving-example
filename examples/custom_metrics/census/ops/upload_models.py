from hydrosdk import Cluster, ModelVersion, LocalModel, DockerImage, SignatureBuilder
from hydrosdk.contract import ProfilingType as PT, ModelContract
from hydrosdk.modelversion import ThresholdCmpOp


cluster = Cluster(
<<<<<<< HEAD
    http_address="<cluster-url>",
=======
    http_address="https://hydro-serving.dev.hydrosphere.io",
>>>>>>> origin/master
)

model_signature = SignatureBuilder("predict") \
    .with_input("age", int, "scalar", PT.NUMERICAL) \
    .with_input("workclass", str, "scalar", PT.CATEGORICAL) \
    .with_input("fnlwgt", int, "scalar", PT.NUMERICAL) \
    .with_input("education", str, "scalar", PT.CATEGORICAL) \
    .with_input("educational-num", int, "scalar", PT.NUMERICAL) \
    .with_input("marital-status", str, "scalar", PT.CATEGORICAL) \
    .with_input("occupation", str, "scalar", PT.CATEGORICAL) \
    .with_input("relationship", str, "scalar", PT.CATEGORICAL) \
    .with_input("race", str, "scalar", PT.CATEGORICAL) \
    .with_input("gender", str, "scalar", PT.CATEGORICAL) \
    .with_input("capital-gain", int, "scalar", PT.NUMERICAL) \
    .with_input("capital-loss", int, "scalar", PT.NUMERICAL) \
    .with_input("hours-per-week", int, "scalar", PT.CATEGORICAL) \
    .with_input("native-country", str, "scalar", PT.CATEGORICAL) \
    .with_output("income", str, "scalar", PT.CATEGORICAL) \
    .build()

model_contract = ModelContract(predict=model_signature)
model_local = LocalModel(
    name="census",
    runtime=DockerImage("hydrosphere/serving-runtime-python-3.7", "2.4.0", None),
    path="../models/model/",
    payload=["src/", "requirements.txt", "model.joblib", "encoders.joblib"],
    contract=model_contract,
    training_data="../data/train.csv",
    install_command="pip install -r requirements.txt"
)
model_mv = model_local.upload(cluster)


metric_signature = SignatureBuilder("predict") \
    .with_input("age", int, "scalar", PT.NUMERICAL) \
    .with_input("workclass", str, "scalar", PT.CATEGORICAL) \
    .with_input("fnlwgt", int, "scalar", PT.NUMERICAL) \
    .with_input("education", str, "scalar", PT.CATEGORICAL) \
    .with_input("educational-num", int, "scalar", PT.NUMERICAL) \
    .with_input("marital-status", str, "scalar", PT.CATEGORICAL) \
    .with_input("occupation", str, "scalar", PT.CATEGORICAL) \
    .with_input("relationship", str, "scalar", PT.CATEGORICAL) \
    .with_input("race", str, "scalar", PT.CATEGORICAL) \
    .with_input("gender", str, "scalar", PT.CATEGORICAL) \
    .with_input("capital-gain", int, "scalar", PT.NUMERICAL) \
    .with_input("capital-loss", int, "scalar", PT.NUMERICAL) \
    .with_input("hours-per-week", int, "scalar", PT.CATEGORICAL) \
    .with_input("native-country", str, "scalar", PT.CATEGORICAL) \
    .with_input("income", str, "scalar", PT.CATEGORICAL) \
    .with_output("value", "double", "scalar", PT.NUMERICAL) \
    .build()

metric_contract = ModelContract(predict=metric_signature)
metric_local = LocalModel(
    name="census_custom_metric",
    runtime=DockerImage("hydrosphere/serving-runtime-python-3.7", "2.4.0", None),
    path="../models/metric/",
    payload=["src/", "requirements.txt", "model.joblib", "encoders.joblib"],
    contract=metric_contract,
    install_command="pip install -r requirements.txt"
)
metric_mv = metric_local.upload(cluster)

# Assign metrics
model_mv.assign_metrics([metric_mv.as_metric(4.236688464332743, ThresholdCmpOp.GREATER_EQ)])
