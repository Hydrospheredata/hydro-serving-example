# Adult model 

This demo contains the model trained on [adult dataset](https://archive.ics.uci.edu/ml/datasets/census+income) to predict whether income exceeds $50K/yr based on census data.
For this model we created two scenarios: 
- model input is a tensor of all 12 features [adult_tensor](model/adult_tensor)
- each feature is a separate input [adult_scalar](model/adult_scalar)

---
- [Model contract(tensor)](model/adult_tensor/serving.yaml) - contains deployment configuration
- [Signature function(tensor)](model/adult_tensor/src/func_main.py) - entry point of model servable.
- [Model contract(scalar)](model/adult_scalar/serving.yaml) - contains deployment configuration
- [Signature function(scalar)](model/adult_scalar/src/func_main.py) - entry point of model servable.
- [Model demo](demo/adult_demo.ipynb) - demo on how to invoke model application

Adult model is stored on remote storage, so before deploying, load it:
```commandline
dvc pull model/random-forest-adult.joblib.dvc
```

## Deployment

```commandline
cd model/adult_TYPE
hs upload
```
