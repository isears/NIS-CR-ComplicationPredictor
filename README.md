# NIS CR Complication Predictor

Code for "Predicting Colonic Neoplasia Surgical Complications: A Machine Learning Approach"

## Organization
Each package contains scripts that output to the cache directory (specified in `localconfig.yaml`). Subsequent components of the pipeline will read from the cache directory.

### Pipeline:
1. Filtering: apply inclusion criteria (e.g. remove all patients younger than 18 years old). Reads from .csv specified in `data_path` config variable. Outputs dataframe to `cache/filtered.csv`
2. Preprocessing: transform data so that it's ready for training (e.g. one-hot-encode ICD diagnoses). Reads from `cache/filtered.csv` and writes to `cache/preprocessed.csv`
3. Modeling: cross-validate models on preprocessed data. Reads from `cache/preprocessed.csv`, writes results to `cache/results` directory (TODO)

Note: a first-pass filter is applied to the entire NIS database before any of these steps. The first-pass filtering script is located in the `standalone` directory.

## Setup

Configure settings by creating a `localconfig.yaml` file in the root directory of the repository with the following format:
```yaml
data_path: '/path/to/local/NIS/data.csv'
cache_path: '/path/to/local/cache/directory'
```

The `cache_path` should point to any emtpy, script-writable directory that can hold intermediate results.

## Run

Various steps of the pipeline are located in respective directories. Run from the top level directory so that scripts have access to other modular components. May have to add the current working directory to the python path as shown below:
```bash
PYTHONPATH=.:$PYTHONPATH python filtering/filterIC.py
```