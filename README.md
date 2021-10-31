# NIS CR Complication Predictor

Code for "Predicting Colonic Neoplasia Surgical Complications: A Machine Learning Approach"

## Setup

Configure settings by creating a `localconfig.yaml` file in the root directory of the repository with the following format:
```yaml
data_path: '/path/to/local/NIS/data.csv'
cache_path: '/path/to/local/cache/directory'
```

## Run

Various steps of the pipeline are located in respective directories. Run from the top level directory so that scripts have access to other modular components. May have to add the current working directory to the python path as shown below:
```bash
PYTHONPATH=.:$PYTHONPATH python filtering/filterIC.py
```