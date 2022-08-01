import pandas as pd
import preprocessing.featureEngineering
import preprocessing.normalization
from preprocessing.parseCCI import get_cci_score
import re


def _baseline_preprocess(df):
    """
    Desired features:
    ---

    Direct from NIS:
        DIED - no change
        LOS - 0 if < 10, 1 if > 10
        AGE - normalize min 18, max 120 (inclusion criteria specified > 18)
        APRDRG_Risk_Mortality - normalize min 1, max 4 (filtering should have removed anything with APRDRG 0
        APRDRG_Severity - same as mortality
        FEMALE - one-hot encode (0, 1, na)
        PAY1 - one-hot encode
        RACE - one-hot encode
        TRAN_IN - one-hot encode
        ZIPINC_QRTL - normalize min 1, max 4

    Engineered:
        lap - whether or not patient had a laparoscopic procedure
        chronic_diabetes - ohe from DX icd codes
        hiv - ohe from DX icd codes
        malignancy - ohe from DX icd codes
        Others??

    NOTE normalization probably doesn't help DTC/RF but may boost LR performance
    """

    icd9_dx_cols = [col for col in df.columns if re.search("^DX[0-9]{1,2}$", col)]
    icd10_dx_cols = [col for col in df.columns if re.search("^I10_DX[0-9]{1,2}$", col)]
    diagnosis_columns = icd9_dx_cols + icd10_dx_cols

    preprocessed_df = pd.DataFrame()

    # Labels
    preprocessed_df['DIED'] = df['DIED']
    preprocessed_df['LOS'] = (df['LOS'] > 10).astype(float)

    anastomotic_leak_codes = ['K632', '56981', 'K651', '56722']
    preprocessed_df['anastomotic_leak'] = df[diagnosis_columns].isin(anastomotic_leak_codes).any(axis='columns').astype(
        float)

    # Normalize
    df = preprocessing.normalization.normalize(df)

    preprocessed_df = pd.concat(
        [preprocessed_df, df[['AGE', 'APRDRG_Risk_Mortality', 'APRDRG_Severity', 'ZIPINC_QRTL']]],
        axis=1
    )

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


def do_preprocessing(df):
    baseline_df = _baseline_preprocess(df)
    # Get OHE chronic conditions
    preprocessed_df = pd.concat([baseline_df, featureEngineering.get_cci_ohe(df)], axis=1)

    return preprocessed_df


def do_cci_preprocessing(df):
    baseline_df = _baseline_preprocess(df)

    # Same as normal, but include MI and CVD codes
    cci_ohe = featureEngineering.get_cci_ohe(df, drop_acute=False)

    # Also compute a CCI score for each patient
    def cci_score(row):
        return get_cci_score(row[row == 1].index.to_list())

    cci_ohe["cci_score"] = cci_ohe.apply(cci_score, axis=1)

    return pd.concat([baseline_df, cci_ohe], axis=1)
