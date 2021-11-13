import yaml
import os

# For compatibility between Pycharm and vanilla command line run configurations
if os.path.exists('./localconfig.yaml'):
    config_path = './localconfig.yaml'
elif os.path.exists('../localconfig.yaml'):
    config_path = '../localconfig.yaml'
else:
    print('[-] Error: Failed to find localconfig.yaml file')


if os.path.exists('./results/README.md'):
    results_path = './results'
elif os.path.exists('../results/README.md'):
    results_path = '../results'
else:
    print('[-] Error: Failed to find results directory')

with open(config_path, 'r') as f:
    SETTINGS = yaml.safe_load(f)