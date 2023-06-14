import re
import pandas as pd

COLONIC_NEOPLASIA_CODES = [
    'D12.0', 'D12.2', 'D12.3', 'D12.4', 'D12.5', 'D12.6', 'K63.5', '211.3', '153.0', '153.1', '153.2', '153.3',
    '153.4', '153.5', '153.6', '153.7', '153.8', '153.9', 'c18.0', 'c18.1', 'c18.2', 'c18.3', 'c18.4', 'c18.5',
    'c18.6', 'c18.7', 'c18.8', 'c18.9'
]


def tell_me_more(has_na):
    """
    Compute demographics statistics about the admissions that have missing values for a specific column

    :param has_na: subset of data to be dropped

    """

    nis_race = {
        0: 'Unknown',
        1: 'White',
        2: 'Black',
        3: 'Hispanic',
        4: 'Asian or Pacific Islander',
        5: 'Native American',
        6: 'Other'
    }

    print('Race:')
    has_na['RACE'] = has_na['RACE'].fillna(0.0)
    has_na['RACE'] = has_na['RACE'].apply(lambda r: nis_race[r])
    print(has_na['RACE'].value_counts(normalize=True))

    print("Age: median (mean +/- std)")
    print(f"{has_na['AGE'].median()} ({has_na['AGE'].mean()} +/- {has_na['AGE'].std()})")

    print("ZIP INC QRTL: median (mean +/- std)")
    print(f"{has_na['ZIPINC_QRTL'].median()} ({has_na['ZIPINC_QRTL'].mean()} +/- {has_na['ZIPINC_QRTL'].std()})")

    print("APRDRG Severity: median (mean +/- std)")
    print(
        f"{has_na['APRDRG_Severity'].median()} ({has_na['APRDRG_Severity'].mean()} +/- {has_na['APRDRG_Severity'].std()})")

    print('DIED:')
    has_na['DIED'] = has_na['DIED'].fillna(0.0)
    print(has_na['DIED'].value_counts(normalize=True))

    print('LOS:')
    print(f"{has_na['LOS'].median()} ({has_na['LOS'].mean()} +/- {has_na['LOS'].std()})")


def do_filter(df_in):
    pd.options.mode.chained_assignment = None  # default='warn'

    over_18 = df_in[df_in['AGE'] > 18]
    print(f'(Age filter) Removed {df_in.shape[0] - over_18.shape[0]} rows, {over_18.shape[0]} remaining')

    elective = over_18[over_18['ELECTIVE'] == 1]
    print(f'(Elective filter) Removed {over_18.shape[0] - elective.shape[0]} rows, {elective.shape[0]} remaining')

    # NIS codes have "implicit" decimals w/trailing blanks
    nis_formatted_codes = [code.replace('.', '').upper() for code in COLONIC_NEOPLASIA_CODES]

    icd9_cols = [col for col in elective.columns if re.search("^DX[0-9]{1,2}$", col)]
    icd10_cols = [col for col in elective.columns if re.search("^I10_DX[0-9]{1,2}$", col)]

    trimmed = elective.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    colonic_neoplasia = trimmed[trimmed[icd9_cols + icd10_cols].isin(nis_formatted_codes).any(axis='columns')]
    print(f'(Colonic neoplasia filter) Removed {elective.shape[0] - colonic_neoplasia.shape[0]} rows, '
          f'{colonic_neoplasia.shape[0]} remaining')

    valid_labels = colonic_neoplasia.dropna(subset=['DIED', 'LOS'])
    print(f'(Label validity filter) Removed {colonic_neoplasia.shape[0] - valid_labels.shape[0]} rows, '
          f'{valid_labels.shape[0]} remaining')

    # merge ZIPINC and ZIPINC_QRTL, then drop rows with missing data
    valid_labels.fillna({'ZIPINC_QRTL': valid_labels['ZIPINC']})
    zip_merged = valid_labels.drop(labels=['ZIPINC'], axis=1)

    valid_features = zip_merged.dropna(subset=['AGE', 'APRDRG_Risk_Mortality', 'APRDRG_Severity', 'ZIPINC_QRTL'])

    print(f'(Feature validity filter) Removed {zip_merged.shape[0] - valid_features.shape[0]} rows, '
          f'{valid_features.shape[0]} remaining')

    valid_aprdrg = valid_features[
        (valid_features['APRDRG_Risk_Mortality'] != 0) & (valid_features['APRDRG_Severity'] != 0)]
    print(f'(APRDRG validity filter) Removed {valid_features.shape[0] - valid_aprdrg.shape[0]} rows, '
          f'{valid_aprdrg.shape[0]} remaining')

    dropped_df = colonic_neoplasia[~colonic_neoplasia.index.isin(valid_aprdrg.index)]
    print(f"Investigating dropped rows ({len(dropped_df)})")
    print("-" * 15)
    tell_me_more(dropped_df)

    return valid_aprdrg
