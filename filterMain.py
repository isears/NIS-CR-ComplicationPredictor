import pandas as pd
import util
from filtering import *

if __name__ == '__main__':
    # Filter by inclusion criteria
    df = pd.read_csv(util.SETTINGS['data_path'], low_memory=False)
    print(f'Starting with {df.shape[0]} admissions')
    filtered_df = filterIC.do_filter(df)

    print('[+] Filtering completed successfully, saving to cache')
    filtered_df.to_csv(f"{util.SETTINGS['cache_path']}/filtered.csv", index=False)
