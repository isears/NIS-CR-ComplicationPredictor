"""
Build separate statsmodels logistic regression models (without SMOTE) and extract odds ratios
"""

import pandas as pd
import util
from modeling import labels
from preprocessing.normalization import denormalize
from scipy.stats import fisher_exact

df = pd.read_csv(f'{util.SETTINGS["cache_path"]}/preprocessed.csv', low_memory=False)
# Throw out normalization
df = denormalize(df)

for label in labels:
    # Convert everything to binary vars (for odds ratios)
    # Over 65
    df['AGE'] = (df['AGE'] > 65).astype(float)
    # APRDRGs > 2
    df['APRDRG_Risk_Mortality'] = (df['APRDRG_Risk_Mortality'] > 2).astype(float)
    df['APRDRG_Severity'] = (df['APRDRG_Severity'] > 2).astype(float)
    # ZIPINC_QRTL < 3
    df['ZIPINC_QRTL'] = (df['ZIPINC_QRTL'] < 2).astype(float)

    # Make sure everything is in 0,1
    assert df.isin([0, 1]).all().all()

    # Clear out anything that doesn't contain any information
    # Only calculate OR for columns with significant positives
    columns_before = df.columns
    df = df.drop(df.columns[df.apply(lambda col: col.sum() < 100)], axis=1)
    # Need at least one labeled in every category
    affected = df[df[label] == 1]
    unaffected = df[df[label] == 0]
    df = df.drop(affected.columns[affected.apply(lambda col: col.sum() == 0)], axis=1)
    dropped_columns = [c for c in columns_before if c not in df.columns]
    print(f'[+] Dropped {len(dropped_columns)} columns for containing no information')

    features_df = df[[c for c in df.columns if c not in labels]]
    odds_ratios = pd.DataFrame(columns=['feature', 'odds', 'p-value'])
    for c in features_df.columns:
        ct = pd.crosstab(df[c], df[label])
        odds, p_value = fisher_exact(ct)
        odds_ratios = odds_ratios.append({'feature': c, 'odds': odds, 'p-value': p_value}, ignore_index=True)

    print('[+] Done')
