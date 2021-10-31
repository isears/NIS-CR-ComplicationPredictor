"""
Filters NIS down to admissions with only colorectal + anastomosis procedures. Expects NIS formated as a directory of CSVs

./FilterByProc.py /path/to/NIS /path/to/output.csv
"""
import glob
import pandas as pd
import re
import math
import sys


def nis_icd9_to_str(x):
    if isinstance(x, float):
        if math.isnan(x):
            return ''

        x = '{0:.0f}'.format(x)

    if len(x) == 3:
        return f'{x[0]}{x[1]}.{x[2]}0'
    elif len(x) == 4:
        return f'{x[0]}{x[1]}.{x[2]}{x[3]}'
    else:
        return ''


def main(src_dir, dst):
    icd10_pc_open = "0DBE0ZZ,0DTH0ZZ,0DTF0ZZ,0DTK0ZZ,0DTL0ZZ,0DTG0ZZ,0DTN0ZZ".split(",")
    icd10_pc_lap = "0DBE3ZZ,0DBGFZZ,0DBLFZZ,0DBMFZZ,0DBNFZZ,0DTMFZZ,0DTLFZZ,0DTGFZZ,0DTNFZZ,0DBE4ZZ,0DTF4ZZ,0DTH4ZZ,0DTL4ZZ,0DTG4ZZ,0DTN4ZZ".split(",")
    icd10_anast_open = "0D1H0ZH,0D1H0ZK,0D1H0ZL,0D1H0ZM,0D1H0ZN,0D1H0ZP,0D1K0ZK,0D1K0ZL,0D1K0ZM,0D1K0ZN,0D1K0ZP,0D1L0ZL,0D1L0ZM,0D1L0ZN,0D1L0ZP,0D1M0ZM,0D1M0ZN,0D1M0ZP,0D1N0ZN,0D1N0ZP,0D190ZL,0D1A0ZH,0D1A0ZK,0D1A0ZL,0D1A0ZM,0D1A0ZN,0D1B0ZH,0D1B0ZK,0D1B0ZL,0D1B0ZM,0D1B0ZN".split(",")
    icd10_anast_lap = "0D1H4ZH,0D1H4ZK,0D1H4ZL,0D1H4ZM,0D1H4ZN,0D1H4ZP,0D1K4ZK,0D1K4ZL,0D1K4ZM,0D1K4ZN,0D1K4ZP,0D1L4ZL,0D1L4ZM,0D1L4ZN,0D1L4ZP,0D1M4ZM,0D1M4ZN,0D1M4ZP,0D1N4ZN,0D1N4ZP,0D194ZL,0D1A4ZH,0D1A4ZK,0D1A4ZL,0D1A4ZM,0D1A4ZN,0D1B4ZH,0D1B4ZK,0D1B4ZL,0D1B4ZM,0D1B4ZN".split(",")

    icd9_pc_open = "45.71 45.72 45.73 45.74 45.75 45.76 45.78".split(" ")
    icd9_pc_lap = "17.31,17.32,17.33,17.34,17.35,17.36,17.39".split(",")
    icd9_anast = "45.94,45.93".split(",")

    icd10_pc = icd10_pc_open + icd10_pc_lap
    icd10_anast = icd10_anast_open + icd10_anast_lap

    icd9_pc = icd9_pc_open + icd9_pc_lap

    icd10_codes = icd10_pc_open + icd10_pc_lap + icd10_anast_open + icd10_anast_lap
    icd9_codes = icd9_pc_open + icd9_pc_lap + icd9_anast

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

        if len(icd9_cols) > 0:  # Need to re-format ICD9 codes
            raw_df[icd9_cols] = raw_df[icd9_cols].applymap(nis_icd9_to_str)

        # Looking for partial colectopy AND anastomosis
        raw_df = raw_df[
            (raw_df[icd9_cols + icd10_cols].isin(icd9_pc + icd10_pc)).any(axis='columns') &
            (raw_df[icd9_cols + icd10_cols].isin(icd9_anast + icd10_anast)).any(axis='columns')
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
