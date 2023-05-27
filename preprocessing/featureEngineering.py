import re
import pandas as pd
from preprocessing.parseCCI import get_comorbidity_codes


# This will not scale very well, could probably benefit from some optimization
def get_chronic(df_in):
    icd9_cols = [col for col in df_in.columns if re.search("^DX[0-9]{1,2}$", col)]
    icd10_cols = [col for col in df_in.columns if re.search("^I10_DX[0-9]{1,2}$", col)]
    df_in[icd10_cols + icd9_cols] = df_in[icd10_cols + icd9_cols].fillna('')

    match_codes, startswith_codes = get_comorbidity_codes()

    print(f'Looking for the following {len(match_codes)} ICD codes (exact match):')
    print(match_codes)

    chronic_match = pd.concat(
        [df_in[icd10_cols + icd9_cols].apply(lambda row: row.eq(dx).any(), axis=1).rename(dx) for dx in
         match_codes], axis=1)

    chronic_match = chronic_match.astype(int)

    print(f'Looking for the following {len(startswith_codes)} ICD codes (prefix match):')
    print(startswith_codes)

    chronic_startswith = pd.concat([df_in[icd10_cols + icd9_cols].apply(
        lambda row: row.str.startswith(code_prefix).any(), axis=1).rename(code_prefix) for code_prefix in
                                    startswith_codes], axis=1)

    chronic_startswith = chronic_startswith.astype(int)

    return pd.concat([chronic_match, chronic_startswith], axis=1)
