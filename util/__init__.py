import yaml
import os

if os.path.exists('./localconfig.yaml'):
    config_path = './localconfig.yaml'
elif os.path.exists('../localconfig.yaml'):
    config_path = '../localconfig.yaml'
else:
    print('[-] Error: Failed to find localconfig.yaml file')


with open(config_path, 'r') as f:
    SETTINGS = yaml.safe_load(f)