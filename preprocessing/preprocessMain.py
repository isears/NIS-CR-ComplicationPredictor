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
    ZIPINC_QRTL - normalize min 1, max 4

Engineered:
    chronic_diabetes - ohe from DX icd codes
    hiv - ohe from DX icd codes
    malignancy - ohe from DX icd codes
    Others??

NOTE normalization probably doesn't help DTC/RF but may boost LR performance
"""

import util
import pandas as pd


def do_preprocessing(df):
    preprocessed_df = pd.DataFrame()

    # Normalize AGE
    preprocessed_df['AGE'] = (df['AGE'] - 18) / (120)
    assert not (preprocessed_df['AGE'] > 1).any()
    assert not (preprocessed_df['AGE'] < 0).any()

    # Normalize APRDRG and ZIPINC_QRTL columns (same range for all of them)
    for four_value_col in ['APRDRG_Risk_Mortality', 'APRDRG_Severity', 'ZIPINC_QRTL']:
        preprocessed_df[four_value_col] = (df[four_value_col] - 1) / 3
        assert not (preprocessed_df[four_value_col] > 1).any()
        assert not (preprocessed_df[four_value_col] < 0).any()

    # One-hot encode FEMALE, PAY1, RACE, TRAN_IN
    dumdums = pd.get_dummies(
        df[['FEMALE', 'PAY1', 'RACE', 'TRAN_IN']],
        columns=['FEMALE', 'PAY1', 'RACE', 'TRAN_IN'],
        prefix={
            'FEMALE': 'sex',
            'PAY1': 'payer',
            'RACE': 'race',
            'TRAN_IN': 'transfer'
        },
        dummy_na=True
    )

    preprocessed_df = pd.concat([preprocessed_df, dumdums], axis=1)

    return preprocessed_df


if __name__ == '__main__':
    filtered_df = pd.read_csv(f"{util.SETTINGS['cache_path']}/filtered.csv")
    do_preprocessing(filtered_df)