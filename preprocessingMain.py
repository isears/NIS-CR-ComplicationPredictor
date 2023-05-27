import util
import pandas as pd
import preprocessing

from concurrent.futures import ProcessPoolExecutor

if __name__ == '__main__':
    executor = ProcessPoolExecutor(max_workers=2)
    lap_filtered = pd.read_csv(f"{util.SETTINGS['cache_path']}/lap_filtered.csv", low_memory=False)
    open_filtered = pd.read_csv(f"{util.SETTINGS['cache_path']}/open_filtered.csv", low_memory=False)

    lap_future = executor.submit(preprocessing.do_preprocessing, lap_filtered)
    open_future = executor.submit(preprocessing.do_preprocessing, open_filtered)

    lap_preprocessed = lap_future.result()
    open_preprocessed = open_future.result()

    lap_preprocessed.to_csv(f"{util.SETTINGS['cache_path']}/lap_preprocessed.csv", index=False)
    open_preprocessed.to_csv(f"{util.SETTINGS['cache_path']}/open_preprocessed.csv", index=False)

    print('[+] Preprocessing completed successfully')
