# NIS CR Complication Predictor

Code for "Predicting Colonic Neoplasia Surgical Complications: A Machine Learning Approach"

Latest results [here](./results/README.md)

## Organization

Each package contains scripts that output to the cache directory (specified in `localconfig.yaml`). Subsequent
components of the pipeline will read from the cache directory.

### Pipeline:

1. Filtering: apply inclusion criteria (e.g. remove all patients younger than 18 years old). Reads from .csv specified
   in `data_path` config variable. Outputs dataframe to `cache/filtered.csv`
2. Preprocessing: transform data so that it's ready for training (e.g. one-hot-encode ICD diagnoses). Reads
   from `cache/filtered.csv` and writes to `cache/preprocessed.csv`
3. Modeling: cross-validate models on preprocessed data. Reads from `cache/preprocessed.csv`, writes results
   to `results` directory

## Setup

Configure settings by creating a `localconfig.yaml` file in the root directory of the repository with the following
format:

```yaml
data_path: '/path/to/local/NIS/data.csv'
cache_path: '/path/to/local/cache/directory'
```

The `cache_path` should point to any emtpy, script-writable directory that can hold intermediate results.

Install python dependencies:

```bash
pip install -r ./requirements.txt
```

## Run

Steps of the pipeline are designed to run independently and save any intermediate results to the cache directory.

```bash
# Run filtering step
python ./filteringMain.py

# Run preprocessing step
python ./preprocessingMain.py

# Run modeling step
python ./modelingMain.py
```