"""
Generate table1 statistics

Requires completion of preprocessing step
"""

import util
import pandas as pd
import os
from docx import Document

# Tuples of (printable name, real column name, filter expression)
T1_ROWS = [
    ('Age > 70', 'AGE', lambda x: x > 70),
    ('% Male', 'sex_0.0', lambda x: x == 1)
]


def write_t1(df: pd.DataFrame):
    document = Document()
    table = document.add_table(rows=1, cols=3)
    table.style = 'Medium Grid 3 Accent 1'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text, hdr_cells[1].text, hdr_cells[2].text = 'Patient Characteristics', 'Laparoscopic', 'Open'

    for idx, (row_name, df_cname, filter_exp) in enumerate(T1_ROWS):
        row_cells = table.add_row().cells
        row_cells[0].text = row_name

        # TODO: Just get total counts for now, but differentiate between lap/open once appropriate edits made to filter
        total_count = len(df[df[df_cname].apply(filter_exp)])
        total_percent = 100 * total_count / len(df.index)

        row_cells[1].text = f'{total_count} ({total_percent:.2f}%)'

    if os.path.exists('results/table1.docx'):
        os.remove('results/table1.docx')

    document.save('results/table1.docx')


if __name__ == '__main__':
    preprocessed_df = pd.read_csv(f'{util.SETTINGS["cache_path"]}/preprocessed.csv')
    write_t1(preprocessed_df)
