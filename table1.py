"""
Generate table1 statistics

Requires completion of preprocessing step
"""

import util
import pandas as pd
from modeling import labels
from preprocessing.normalization import denormalize
from preprocessing.parseCCI import get_labeled_comorbidity_codes
import os
from docx import Document

AGE_CUTOFF = 65
# Tuples of (printable name, real column name, filter expression)
# T1_ROWS = [
#     ('Age > 70', 'AGE', lambda x: x > 70),
#     ('% Male', 'sex_0.0', lambda x: x == 1)
# ]

feature_name_map = {
    'AGE': f'Age > {AGE_CUTOFF}',
    'ZIPINC_QRTL': 'Median household income for patient\'s ZIP Code',
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

def make_tf_df():
    #read in open and lap preprocessed

    lap_percent_df = pd.DataFrame()
    lap_abs_df = pd.DataFrame()
    open_percent_df = pd.DataFrame()
    open_abs_df = pd.DataFrame()

    for ds in ['lap', 'open']:
        ##ISAAC'S CODE FOR TABLE3
        df = pd.read_csv(f'{util.SETTINGS["cache_path"]}/{ds}_preprocessed.csv', low_memory=False)
        #df = pd.read_csv(f'{util.SETTINGS["cache_path"]}/lap_preprocessed.csv', low_memory=False)
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

        ##NEW CODE THAT ISHAANI's ADDED + WRITTEN
        if ds == "lap":
            lap_abs_df = df.sum()
            lap_percent_df = round(df.mean() * 100, 2)
        if ds == "open":
            open_abs_df = df.sum()
            open_percent_df = round(df.mean() * 100, 2)

    #making filled in df, with 4 columns (see tmp_col_names)
    df = pd.concat([lap_abs_df, lap_percent_df, open_abs_df, open_percent_df], axis=1)
    tmp_col_names = ["Laparoscopic (#)", "Laparoscopic (%)", "Open (#)", "Open (%)"]
    df.columns = tmp_col_names

    #reformatting the final 2 columsn like table 1, dropping the old columns
    df["Laparoscopic"] = df["Laparoscopic (#)"].astype(str) + " (" + df["Laparoscopic (%)"].astype(str) + "%)"
    df["Open"] = df["Open (#)"].astype(str) + " (" + df["Open (%)"].astype(str) + "%)"
    df.drop(tmp_col_names, axis=1, inplace=True)

    #writing to a csv, table1.csv
    df.to_csv("table1.csv", index=True)

    #putting it in the format like Table 1 we're trying to emulate

#old code, didn't use at all
# def write_t1(df: pd.DataFrame):
#     document = Document()
#     table = document.add_table(rows=1, cols=3)
#     table.style = 'Medium Grid 3 Accent 1'
#     hdr_cells = table.rows[0].cells
#     hdr_cells[0].text, hdr_cells[1].text, hdr_cells[2].text = 'Patient Characteristics', 'Laparoscopic', 'Open'
#
#     for idx, (row_name, df_cname, filter_exp) in enumerate(T1_ROWS):
#         row_cells = table.add_row().cells
#         row_cells[0].text = row_name
#
#         # TODO: Just get total counts for now, but differentiate between lap/open once appropriate edits made to filter
#         total_count = len(df[df[df_cname].apply(filter_exp)])
#         total_percent = 100 * total_count / len(df.index)
#
#         row_cells[1].text = f'{total_count} ({total_percent:.2f}%)'
#
#     if os.path.exists('results/table1.docx'):
#         os.remove('results/table1.docx')
#
#     document.save('results/table1.docx')

if __name__ == '__main__':
    #preprocessed_df = pd.read_csv(f'{util.SETTINGS["cache_path"]}/preprocessed.csv')
    make_tf_df()
