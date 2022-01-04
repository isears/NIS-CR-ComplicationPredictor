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
from scipy import stats
from docx import Document
from numpy import array
import numpy as np

CONFIDENCE = 0.95
AGE_CUTOFF = 65

feature_name_map = {
    'AGE': f'Age > {AGE_CUTOFF}',
    'ZIPINC_QRTL': 'Median household income for patient\'s ZIP Code',
    'lap': 'Laparoscopic procedure',
    'sex_0.0': 'Male',
    'sex_1.0': 'Female',
    'sex_nan': 'Unknown sex',
    'payer_1.0': 'Medicare primary payer',
    'payer_2.0': 'Medicaid primary payer',
    'payer_3.0': 'Private insurance primary payer',
    'payer_4.0': 'Self-pay primary payer',
    'payer_5.0': 'No charge',
    'payer_6.0': 'Other primary payer',
    'payer_nan': 'Unknown primary payer',
    'race_1.0': 'White',
    'race_2.0': 'Black',
    'race_3.0': 'Hispanic',
    'race_4.0': 'Asian or Pacific Islander',
    'race_5.0': 'Native American',
    'race_6.0': 'Other',
    'race_nan': 'Unknown race',
    'transfer_0.0': 'Not transferred',
    'transfer_1.0': 'Transferred from acute care hospital',
    'transfer_2.0': 'Transferred from another type of health facility',
    'transfer_nan': 'Unknown transfer status'
}

df = pd.read_csv(f'{util.SETTINGS["cache_path"]}/preprocessed.csv', low_memory=False)
# Throw out normalization
df = denormalize(df)

# Convert everything to binary vars (for odds ratios)
# Over 65
df['AGE'] = (df['AGE'] > AGE_CUTOFF).astype(int)
# APRDRGs > 2
df['APRDRG_Risk_Mortality'] = (df['APRDRG_Risk_Mortality'] > 2).astype(int)
df['APRDRG_Severity'] = (df['APRDRG_Severity'] > 2).astype(int)
# ZIPINC_QRTL < 3
df['ZIPINC_QRTL'] = (df['ZIPINC_QRTL'] < 2).astype(int)

df = df.rename(columns=feature_name_map)

for label in labels:
    df[label] = df[label].astype(int)

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
    df[cci_category] = (df[f'match_{cci_category}'] | df[f'startswith_{cci_category}']).astype(int)
    df = df.drop([f'match_{cci_category}', f'startswith_{cci_category}'], axis=1)

# Make sure everything is in 0,1
assert df.isin([0, 1]).all().all()

# Setup table
document = Document()
table = document.add_table(rows=2 + (len(df.columns) - len(labels)), cols=len(labels) + 1)
# table.style = 'Medium Grid 3 Accent 1'
table.style = 'Table Grid'
hdr_cells = table.rows[0].cells
hdr_cell_left = hdr_cells[0]
hdr_cell_left.text = 'Preoperative Characteristics'

hdr_cell_right = hdr_cells[1]
for cell in hdr_cells[2:]:
    hdr_cell_right = hdr_cell_right.merge(cell)

hdr_cell_right.text = 'Odds Ratio; p-value'
categories_list = [c for c in df.columns if c not in labels]
category_to_row_map = {category: idx + 2 for idx, category in enumerate(categories_list)}
label_to_column_map = {label: idx + 1 for idx, label in enumerate(labels)}

for category, idx in category_to_row_map.items():
    table.rows[idx].cells[0].text = category

for label, idx in label_to_column_map.items():
    table.rows[1].cells[idx].text = label

all_dropped_columns = set()

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
    all_dropped_columns = all_dropped_columns.union(set(dropped_columns))

    features_df = cleaned_df[[c for c in cleaned_df.columns if c not in labels]]
    all_odds = []
    for c in features_df.columns:
        ct = pd.crosstab(cleaned_df[c], cleaned_df[label])
        odds, p_value = fisher_exact(ct) # odds ratio
        all_odds.append(odds)
        relevant_row = table.rows[category_to_row_map[c]]

        alpha = 0.01
        if p_value < alpha:
            relevant_row.cells[label_to_column_map[label]].text = f'{odds:.2f}; < {alpha}'
        else:
            relevant_row.cells[label_to_column_map[label]].text = f'{odds:.2f}; {p_value:.3f}'
    odds_ci = stats.t.interval(alpha=CONFIDENCE, df=len(all_odds)-1 , loc=np.mean(all_odds), scale=stats.sem(all_odds))


# Drop features that ended up being irrelevant to odds ratio calculation
for col in sorted(list(all_dropped_columns), key=lambda x: category_to_row_map[x], reverse=True):
    row_to_remove = table.rows[category_to_row_map[col]]
    row_to_remove._element.getparent().remove(row_to_remove._element)

if os.path.exists('results/table3.docx'):
    os.remove('results/table3.docx')

document.save('results/table3.docx')
print('[+] Done')
