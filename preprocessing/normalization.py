import pandas as pd

NORMALIZATION_MAX_AGE = 120
NORMALIZATION_MIN_AGE = 18


def normalize(df: pd.DataFrame):
    # Normalize AGE
    df['AGE'] = (df['AGE'] - NORMALIZATION_MIN_AGE) / NORMALIZATION_MAX_AGE
    assert not (df['AGE'] > 1).any()
    assert not (df['AGE'] < 0).any()

    # Normalize APRDRG and ZIPINC_QRTL columns (same range for all of them)
    for four_value_col in ['APRDRG_Risk_Mortality', 'APRDRG_Severity', 'ZIPINC_QRTL']:
        df[four_value_col] = (df[four_value_col] - 1) / 3
        assert not (df[four_value_col] > 1).any()
        assert not (df[four_value_col] < 0).any()

    return df


def denormalize(df: pd.DataFrame):
    df['AGE'] = (df['AGE'] * NORMALIZATION_MAX_AGE) + NORMALIZATION_MIN_AGE

    for four_value_col in ['APRDRG_Risk_Mortality', 'APRDRG_Severity', 'ZIPINC_QRTL']:
        df[four_value_col] = (df[four_value_col] * 3) + 1

    return df
