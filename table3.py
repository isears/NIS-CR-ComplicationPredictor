"""
Build separate statsmodels logistic regression models (without SMOTE) and extract odds ratios
"""

import pandas as pd
import util
import os
from modeling import labels
from preprocessing.normalization import denormalize
from preprocessing.parseCCI import get_labeled_comorbidity_codes
from scipy.stats import fisher_exact
from docx import Document

TOP_FEATURES_TO_SHOW = 15

df = pd.read_csv(f'{util.SETTINGS["cache_path"]}/preprocessed.csv', low_memory=False)
# Throw out normalization
df = denormalize(df)

# Convert everything to binary vars (for odds ratios)
# Over 65
df['AGE'] = (df['AGE'] > 65).astype(int)
# APRDRGs > 2
df['APRDRG_Risk_Mortality'] = (df['APRDRG_Risk_Mortality'] > 2).astype(int)
df['APRDRG_Severity'] = (df['APRDRG_Severity'] > 2).astype(int)
# ZIPINC_QRTL < 3
df['ZIPINC_QRTL'] = (df['ZIPINC_QRTL'] < 2).astype(int)

# Convert raw CCI codes back to their general category
labeled_match_codes, labeled_startswith_codes = get_labeled_comorbidity_codes()
all_cci_categories = set(labeled_match_codes.keys()).union(set(labeled_startswith_codes.keys()))
analyzed_codes = set()

for cci_category, codes in labeled_match_codes.items():
    valid_codes = [c for c in codes if c in df.columns]
    df[f'match_{cci_category}'] = df[valid_codes].sum(axis=1) > 0
    analyzed_codes = analyzed_codes.union(set(valid_codes))

for cci_category, codes in labeled_startswith_codes.items():
    valid_codes = [c for c in codes if c in df.columns]
    df[f'startswith_{cci_category}'] = df[valid_codes].sum(axis=1) > 0
    analyzed_codes = analyzed_codes.union(set(valid_codes))

df = df.drop(analyzed_codes, axis=1)

for cci_category in all_cci_categories:
    assert df[f'match_{cci_category}'].dtype.name == 'bool'
    assert df[f'startswith_{cci_category}'].dtype.name == 'bool'
    df[cci_category] = df[f'match_{cci_category}'] | df[f'startswith_{cci_category}'].astype(int)
    df = df.drop([f'match_{cci_category}', f'startswith_{cci_category}'], axis=1)

# Make sure everything is in 0,1
assert df.isin([0, 1]).all().all()

# Setup table
document = Document()
table = document.add_table(rows=1 + len(df.columns), cols=len(labels) + 1)
table.style = 'Medium Grid 3 Accent 1'
hdr_cells = table.rows[0].cells
hdr_cell_left = hdr_cells[0]
hdr_cell_left.text = 'Preoperative Characteristics'

hdr_cell_right = hdr_cells[1]
for cell in hdr_cells[2:]:
    hdr_cell_right = hdr_cell_right.merge(cell)

hdr_cell_right.text = 'Odds Ratio; p-value'

for idx, label in enumerate(labels):

    # Clear out anything that doesn't contain any information
    # Only calculate OR for columns with significant positives
    original_columns = df.columns
    cleaned_df = df.drop(df.columns[df.apply(lambda col: col.sum() < 100)], axis=1)
    # Need at least one labeled in every category
    affected = cleaned_df[cleaned_df[label] == 1]
    unaffected = cleaned_df[cleaned_df[label] == 0]
    cleaned_df = cleaned_df.drop(affected.columns[affected.apply(lambda col: col.sum() == 0)], axis=1)
    dropped_columns = [c for c in original_columns if c not in cleaned_df.columns]
    print(f'[*] Dropped {len(dropped_columns)} columns for containing no information, {len(cleaned_df.columns)} remain')
    print(dropped_columns)

    features_df = cleaned_df[[c for c in cleaned_df.columns if c not in labels]]
    odds_ratios = pd.DataFrame(columns=['feature', 'odds', 'p-value'])
    for c in features_df.columns:
        ct = pd.crosstab(cleaned_df[c], cleaned_df[label])
        odds, p_value = fisher_exact(ct)
        odds_ratios = odds_ratios.append({'feature': c, 'odds': odds, 'p-value': p_value}, ignore_index=True)

    # Add information to table
    for row in table.rows:
        row_cells = row.cells

if os.path.exists('results/table3.docx'):
    os.remove('results/table3.docx')

document.save('results/table3.docx')
print('[+] Done')