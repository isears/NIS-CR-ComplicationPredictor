"""
Initial filter of NIS down to admissions with a partial colectomy + anastomosis.
Resulting dataset is much easier to work with as it is < 1% of NIS.
Should yield 35,708 admissions

./FilterByProc.py /path/to/NIS /path/to/output.csv
"""
import glob
import pandas as pd
import re
import sys
import util


def main(src_dir, dst):
    df = pd.DataFrame()
    csvs_to_read = len(glob.glob(f'{src_dir}/*.csv'))
    no_hits_list = list()

    for idx, csv in enumerate(glob.glob(f'{src_dir}/*.csv')):
        print(f'Reading: {csv}')

        raw_df = pd.read_csv(csv, low_memory=False)
        print(f'Initial length: {len(raw_df.index)}')

        icd9_cols = [col for col in raw_df.columns if re.search("^PR[0-9]{1,2}$", col)]
        icd10_cols = [col for col in raw_df.columns if re.search("^I10_PR[0-9]{1,2}$", col)]

        print(f'Got {len(icd9_cols)} ICD9 procedure columns and {len(icd10_cols)} ICD10 procedure columns')

        # Looking for partial colectopy AND anastomosis
        raw_df = raw_df[
            (raw_df[icd9_cols + icd10_cols].isin(util.inclusionCriteria.get_all_pc())).any(axis='columns') &
            (raw_df[icd9_cols + icd10_cols].isin(util.inclusionCriteria.get_all_anast())).any(axis='columns')
            ]

        print(f'Final length: {len(raw_df.index)}')

        if len(raw_df.index) == 0:
            no_hits_list.append(csv)

        df = df.append(raw_df)
        print(f'[+] Progress: {idx} / {csvs_to_read}')

    print(f'Final size: {len(df.index)}')
    print(f'{len(no_hits_list)} files had 0 hits:')
    print(no_hits_list)
    df.to_csv(dst)


if __name__ == '__main__':
    src_dir = sys.argv[1]
    dst = sys.argv[2]
    main(src_dir, dst)
