import pandas as pd
import util
import filtering
import re

if __name__ == '__main__':
    # Filter by inclusion criteria
    df = pd.read_csv(util.SETTINGS['data_path'], low_memory=False)
    print(f'Starting with {df.shape[0]} admissions')

    icd9_proc_cols = [col for col in df.columns if re.search("^PR[0-9]{1,2}$", col)]
    icd10_proc_cols = [col for col in df.columns if re.search("^I10_PR[0-9]{1,2}$", col)]
    procedure_columns = icd9_proc_cols + icd10_proc_cols

    lap_df = df[df[procedure_columns].isin(util.inclusionCriteria.get_all_lap()).any(axis='columns')]
    open_df = df[~df[procedure_columns].isin(util.inclusionCriteria.get_all_lap()).any(axis='columns')]

    assert len(lap_df) + len(open_df) == len(df), '[-] Lap/Open split was uneven, check logic'
    assert len(lap_df) > 0
    assert len(open_df) > 0

    print('[*] Filtering laparoscopic dataset')
    lap_filtered = filtering.do_filter(lap_df)
    print('[+] Filtering completed successfully, saving to cache')
    lap_filtered.to_csv(f"{util.SETTINGS['cache_path']}/lap_filtered.csv", index=False)

    print('[*] Filtering open dataset')
    open_filtered = filtering.do_filter(open_df)
    print('[+] Filtering completed successfully, saving to cache')
    open_filtered.to_csv(f"{util.SETTINGS['cache_path']}/open_filtered.csv", index=False)
