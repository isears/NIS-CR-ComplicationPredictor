import util
import pandas as pd
import preprocessing

if __name__ == '__main__':
    filtered_df = pd.read_csv(f"{util.SETTINGS['cache_path']}/filtered.csv", low_memory=False)
    preprocessed_df = preprocessing.do_preprocessing(filtered_df)

    print('[+] Preprocessing completed successfully, saving to cache')
    preprocessed_df.to_csv(f"{util.SETTINGS['cache_path']}/preprocessed.csv", index=False)
