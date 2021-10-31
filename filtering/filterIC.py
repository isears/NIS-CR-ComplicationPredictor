import re
import pandas as pd
import util

COLONIC_NEOPLASIA_CODES = [
    'D12.0', 'D12.2', 'D12.3', 'D12.4', 'D12.5', 'D12.6', 'K63.5', '211.3', '153.0', '153.1', '153.2', '153.3',
    '153.4', '153.5', '153.6', '153.7', '153.8', '153.9', 'c18.0', 'c18.1', 'c18.2', 'c18.3', 'c18.4', 'c18.5',
    'c18.6', 'c18.7', 'c18.8', 'c18.9'
]


def do_filter(df_in):
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
    print(f'(Validity filter) Removed {colonic_neoplasia.shape[0] - valid_labels.shape[0]} rows, '
          f'{valid_labels.shape[0]} remaining')

    return valid_labels


if __name__ == '__main__':
    # Filter by inclusion criteria
    df = pd.read_csv(util.SETTINGS['data_path'], low_memory=False)
    print(f'Starting with {df.shape[0]} admissions')
    filtered_df = do_filter(df)

    print('[+] Filtering completed successfully, saving to cache')
    filtered_df.to_csv(f"{util.SETTINGS['cache_path']}/filtered.csv", index=False)