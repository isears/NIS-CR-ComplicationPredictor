import yaml

with open('./settings.yaml', 'r') as f:
    SETTINGS = yaml.safe_load(f)