# ML Runtime

ML runtime is a small server that can import pre-trained user model and serve
it via unified HTTP API.

## HTTP API
For now, the main access point of runtimes is
`POST /<entry_point>` method.

### Request body example

| sepal length (cm) | sepal width (cm) | petal length (cm) | petal width (cm) | features  | color |
|-------------------|------------------|-------------------|------------------|-----------|-------|
|        5.0        |        3.0       |        1.6        |        0.2       |[1,2,3,4,5]|   12  |
|        5.9        |        3.0       |        5.1        |        1.8       |[8,0,5,1,7]|   1   |

This dataframe can be represented in row-wise column list:

```
[
  {
    "sepal length (cm)": 5.0,
    "sepal width (cm)": 3.0,
    "petal length (cm)": 1.6,
    "petal width (cm)": 0.2,
    "features": [ 1, 2, 3, 4, 5],
    "color": 12,
  },
  {
    "sepal length (cm)": 5.9,
    "sepal width (cm)": 3.0,
    "petal length (cm)": 5.1,
    "petal width (cm)": 1.8,
    "features": [8, 0, 5, 1, 7],
    "color": 1,
  }
]
```

That is unified input structure for all runtimes.

## Model retrieval
Every runtime expects model in the `/model` repository.

## HTTP parameters
Runtime HTTP server parameters are set up with `SERVE_ADDR` and `SERVE_PORT` environment variables. Their defaults are `0.0.0.0` and `9090` respectively.

## Implemented runtimes
* [sklearn](scikit/)
* [sklearn for databricks](databricks_python2/)
* [spark-ml (local imlpementation)](localml-spark/)
* [python3](function_py/)
* [tensorflow](tensorflow/)
