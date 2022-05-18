'''
Created by @raceee on request of the standard deviation of the data. This script can be a place for all on demand stats on the project
'''

import pandas as pd
import yaml

with open("localconfig.yaml", "r") as yamlfile:
    data = yaml.load(yamlfile)

def get_std(df):
    return df.std()

if __name__ == "__main__":
    med_df = pd.read_csv(data["filtered"])
    print(get_std(med_df))