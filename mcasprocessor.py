import argparse
import time
from pathlib import Path

import pandas as pd

# ======= USER DEFINED VARIABLES ======== #
filename_to_process = None

# columns to load from the input csv
columns_of_interest = ['sasid', 'stugrade', 'eperf2', 'mperf2', 'sperf2', 'escaleds',
                       'mscaleds', 'sscaleds', 'ecpi', 'mcpi', 'scpi']

# subjects used to seperate records
subjects = ['ela', 'math', 'science']

# Ellevation canonical format
output_column_format = ['NCESID', 'StudentTestID', 'StudentLocalID', 'StudentGradeLevel',
                        'TestDate', 'TestName', 'TestTypeName', 'TestSubjectName', 'TestGradeLevel',
                        'Score1Label', 'Score1Type', 'Score1Value',
                        'Score2Label', 'Score2Type', 'Score2Value',
                        'Score3Label', 'Score3Type', 'Score3Value',
                        'Score4Label', 'Score4Type', 'Score4Value'
                        ]
# ======================================= #


class MCASProcessor:
    """Processor to convert MCAS CSV files to Ellevation canonical format"""

    def __init__(self):
        pass

    def create_subject_df(self, df, subject):
        """Creates a dataframe for each test subject

        Parameters
        ----------
        df : pd.DataFrame
            Input DataFrame used to create `subject` DataFrames from.

        subject : str {'ela', 'math', 'science'}
            Name of the test subject to use to create the DataFrame

        Returns
        -------
        df : pd.DataFrame
             DataFrame from test `subject`.
        """
        supported_subjects = {
            'ela': {
                'name': 'ELA',
                'abbrev': 'e',
                'test_date': '4/1/20'
            },
            'math': {
                'name': 'Math',
                'abbrev': 'm',
                'test_date': '5/1/20'
            },
            'science': {
                'name': 'Science',
                'abbrev': 's',
                'test_date': '6/1/20'
            }
        }
        try:
            sub = supported_subjects[subject]
        except KeyError:
            raise KeyError(f'Please select a subject in: {supported_subjects.keys()}')

        subject_df = pd.DataFrame()
        subject_df['StudentTestID'] = df.sasid
        subject_df['NCESID'] = 373737
        subject_df['StudentLocalID'] = ' '
        subject_df['StudentGradeLevel'] = df.stugrade
        subject_df['TestDate'] = sub['test_date']
        subject_df['TestName'] = 'MCAS'
        subject_df['TestTypeName'] = f'MCAS {sub["name"]}'
        subject_df['TestSubjectName'] = f'{sub["name"]}'
        subject_df['TestGradeLevel'] = df.stugrade
        subject_df['Score1Label'] = 'Performance Level'
        subject_df['Score1Type'] = 'Level'
        subject_df['Score1Value'] = df[f'{sub["abbrev"]}perf2']
        subject_df['Score2Label'] = 'Scaled Score'
        subject_df['Score2Type'] = 'Scale'
        subject_df['Score2Value'] = df[f'{sub["abbrev"]}scaleds']
        subject_df['Score3Label'] = 'CPI'
        subject_df['Score3Type'] = 'Scale'
        subject_df['Score3Value'] = df[f'{sub["abbrev"]}cpi']
        subject_df['Score4Label'] = ' '
        subject_df['Score4Type'] = ' '
        subject_df['Score4Value'] = ' '

        return subject_df

    def create_combined_subject_dfs(self, df, subjects=None):
        """Combines the DataFrames created by `create_subject_df`"""
        combined_df = pd.DataFrame()
        for subject in subjects:
            subject_df = self.create_subject_df(df=df, subject=subject)
            combined_df = pd.concat([combined_df, subject_df])
        return combined_df

    def remove_rows_with_blankspace_test_scores(self, df):
        """Removes rows where there is a blank space (' ') in
        the test value columns.

        This function will remove ONLY rows that are missing
        all three test values.
        """
        df_copy = df.copy()
        spaces_mask = df.Score1Value.str.isspace() \
            & df.Score2Value.str.isspace() \
            & df.Score3Value.str.isspace()
        return df_copy.loc[~spaces_mask, :]

    def correct_performance_level_value(self, df):
        """Remap performance level column values"""
        perf_level_map = {
            'F': '1 - F',
            'W': '2 - W',
            'NI': '3 - NI',
            'P': '4 - P',
            'A': '5 - A',
            'P+': '6 - P+',
            ' ': ' '
        }
        df['Score1Value'] = df['Score1Value'].map(perf_level_map)
        return df

    def reorder_df_columns(self, df, column_list):
        """Match the format of the Ellevation input format"""
        return df[column_list]


def get_filename():
    """Where to search for the filename to process

    Order of Precedence:
    1. --filename command line flag
    2. defined in 'USER DEFINED VARIABLES' in `processor.py`
    3. Ask user for CLI input after running `process.py`
    """
    if args.filename:
        filename = Path(args.filename)
    elif filename_to_process:
        filename = Path(filename_to_process)
    else:
        filename = Path(input('Please enter the filename to process: '))
    return filename


def main():
    filename = get_filename()
    start = time.time()
    print(f'Processing: {filename}')
    df = pd.read_csv(filename, usecols=columns_of_interest)
    process = MCASProcessor()
    df = process.create_combined_subject_dfs(df, subjects=subjects)
    df = process.remove_rows_with_blankspace_test_scores(df)
    df = process.correct_performance_level_value(df)
    df = process.reorder_df_columns(df, column_list=output_column_format)
    df.to_csv(f'{filename.stem}_pyprocessed.csv', index=False)
    print('DONE')
    print(f'Elapsed time: {round(time.time() - start, 4)} seconds')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Processor for MCAS Files')
    parser.add_argument('--filename', nargs='?', help='filename to process')
    args = parser.parse_args()

    main()
