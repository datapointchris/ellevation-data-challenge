import os
import time
from pathlib import Path

import pandas as pd

import mcasprocessor

# ======= USER DEFINED VARIABLES ======== #
input_folder = Path('dummy_data')

output_folder = Path('processed_data')

# ======================================= #
columns_of_interest = mcasprocessor.columns_of_interest
subjects = mcasprocessor.subjects
output_column_format = mcasprocessor.output_column_format

program_start = time.time()

os.makedirs(output_folder, exist_ok=True)

files = input_folder.glob('*.csv')

for filename in files:
    print(f'Processing: {filename}')
    df = pd.read_csv(filename, usecols=columns_of_interest)
    process = mcasprocessor.MCASProcessor()
    df = process.create_combined_subject_dfs(df, subjects=subjects)
    df = process.remove_rows_with_blankspace_test_scores(df)
    df = process.correct_performance_level_value(df)
    df = process.reorder_df_columns(df, column_list=output_column_format)
    df.to_csv(f'{output_folder / filename.stem}_batchprocessed.csv', index=False)

print('FINISHED BATCH PROCESSING')
print(f'TOTAL Elapsed time: {round(time.time() - program_start, 4)} seconds')
