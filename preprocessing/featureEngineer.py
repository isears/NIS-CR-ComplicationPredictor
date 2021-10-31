import re
import pandas as pd

# For now, just diabetesChronic
CHRONIC_CONDITIONS_ICD9 = [
    "25040", "25041", "25042", "25043", "25050", "25051", "25052", "25053", "25060", "25061", "25062", "25063"
]

CHRONIC_CONDITIONS_ICD10 = [
    "E1129", "E1121", "E1165", "E1021", "E1065", "E11311", "E11319", "E1136", "E1139", "E10311", "E10319", "E1036",
    "E1037X1", "E1037X2", "E1037X3", "E1037X9", "E1039", "E1065", "E1140", "E1040"
]

CHRONIC_CONDITIONS = CHRONIC_CONDITIONS_ICD9 + CHRONIC_CONDITIONS_ICD10


def get_chronic(df_in):
    icd9_cols = [col for col in df_in.columns if re.search("^DX[0-9]{1,2}$", col)]
    icd10_cols = [col for col in df_in.columns if re.search("^I10_DX[0-9]{1,2}$", col)]

    chronic = pd.DataFrame()

    for dx in CHRONIC_CONDITIONS:
        chronic[dx] = df_in[icd10_cols + icd9_cols].apply(lambda row: 1 if dx in row else 0, axis=1)

    return chronic