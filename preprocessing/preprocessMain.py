"""
Desired features:
---

Direct from NIS:
    AGE - normalize min 18, max 120 (inclusion criteria specified > 18)
    APRDRG_Risk_Mortality - normalize min 1, max 4 (filtering should have removed anything with APRDRG 0
    APRDRG_Severity - same as mortality
    FEMALE - one-hot encode (0, 1, na)
    PAY1 - one-hot encode
    RACE - one-hot encode
    TRAN_IN - one-hot encode
    ZIPINC - one-hot encode
    ZIPINC_QRTL - one-hot encode

Engineered:
    chronic_diabetes - ohe from DX icd codes
    hiv - ohe from DX icd codes
    malignancy - ohe from DX icd codes
    Others??
"""

import util
import pandas as pd


def do_preprocessing(df):
    preprocessed_df = pd.DataFrame()

    # Normalize AGE
    preprocessed_df['AGE'] = (df['AGE'] - 18) / (120)
    assert not (preprocessed_df['AGE'] > 1).any()

    # Normalize APRDRG columns
    for aprdrg in ['APRDRG_Risk_Mortality', 'APRDRG_Severity']:
        preprocessed_df[aprdrg] = (df[aprdrg] - 1) / 3
        assert not (preprocessed_df[aprdrg] > 1).any()

    return preprocessed_df


if __name__ == '__main__':
    filtered_df = pd.read_csv(f"{util.SETTINGS['cache_path']}/filtered.csv")
    do_preprocessing(filtered_df)