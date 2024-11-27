import pandas as pd
import plotly.express as px
import numpy as np
import os

SPARSENESS_THRESHOLD = 0.99 # All columns where there are (SPARSENESS_THRESHOLD * 100)% n/a values will be dropped
NEW_DATA_ONLY = True # If True, all data entries preceding 2002 will be dropped


def drop_redudant_columns(df):
    """Drops columns that convey info already present in other existing columns."""

    df = df.drop(columns=["IYR", "IYR2", "IYR3", "YEAR", "IMO", "IMO2", "IMO3",
                          "CASINJRR", "CASKLDRR"], axis=1, errors='ignore')
    df.rename(columns={'YEAR4': 'YEAR'}, inplace=True)
    return df


def drop_dummy_columns(df):
    """Drops dummy columns."""
    return df.drop(columns=["DUMMY1", "DUMMY2", "DUMMY3", "DUMMY4", "DUMMY5", "DUMMY6", 
                            "ADJUNCT1", "ADJUNCT2", "ADJUNCT3", "SSB1", "SSB2"], axis=1, errors='ignore')
    

def drop_old_entries(df):
    """Drop all entries preceding 2002."""

    count_old = df[df['YEAR'] < 2002].shape[0]
    count_new = df[df['YEAR'] >= 2002].shape[0]
    print(f"Deleting {count_old} records from 2001 or earlier, {count_new} records remain.")
    return df[df['YEAR'] >= 2002]


def drop_sparse_columns(df, threshold):
    """Drops all columns with a null entry ratio greater than a given threshold."""

    # Calculate the null rate for each column
    null_rates = df.isna().mean()
    # Filter column names where the null rate exceeds the threshold
    high_null_columns = null_rates[null_rates > threshold].index.tolist()
    return df.drop(columns=high_null_columns, axis=1, errors='ignore')


def merge_narration(df):
    """Merges all "NARRx" columns into a single "NARR" text column."""

    def merge_row_narration(row):
        narration = ""
        # Iterate through NARR1 to NARR15 columns
        for i in range(1, 16):
            narr_column = f'NARR{i}'
            if narr_column in row and pd.notna(row[narr_column]):
                narration += str(row[narr_column])
        return narration.strip()  # Remove any trailing space
    
    if 'NARR' in df.columns:
        return df
    else:
        df['NARR'] = df.apply(merge_row_narration, axis=1)
        df = df.drop(columns = ['NARRLEN'], axis=1, errors='ignore')
        return df.drop(columns=[f'NARR{i}' for i in range(1, 16) if f'NARR{i}' in df.columns], axis=1, errors='ignore')
    

def filter_measure_errors(df):
    """Filters entries of incidents with the same id that happened at the same time
        so that only the entry with the least amount of null features remains in the dataset."""
    
    def get_best_entry(group):
        non_null_ratio = group.notnull().mean(axis=1)
        return group.loc[non_null_ratio.idxmax()]
    
    grouped = df.groupby(['INCDTNO', 'YEAR', 'MONTH', 'DAY', 'TIMEHR', 'TIMEMIN'])
    return grouped.apply(get_best_entry).reset_index(drop=True)
    

def format_columns(df):
    """Formats column values in easier to manage types."""
    
    df['PASSTRN'] = df['PASSTRN'].replace({'Y': True, 'N': False}).fillna(False)
    df['LOADED1'] = df['LOADED1'].replace({'Y': True, 'N': False})
    df['LOADED2'] = df['LOADED2'].replace({'Y': True, 'N': False})
    df['EQATT'] = df['EQATT'].replace({'Y': True, 'N': False})
    return df

def create_datetime_column(df):
    """Creates a datetime type column to have all time info in one place, also allowing sorting of the dataset by incident time."""

    df['TIMEHR'] = df['TIMEHR'].astype(str).str.replace(r'\.0$', '', regex=True)
    df['TIMEMIN'] = df['TIMEMIN'].astype(str).str.replace(r'\.0$', '', regex=True)
    df['TIMEHR'] = df['TIMEHR'].str.zfill(2)  
    df['TIMEMIN'] = df['TIMEMIN'].str.zfill(2) 
    
    # Combine YEAR, MONTH, DAY, TIMEHR, TIMEMIN, and AMPM into a single datetime string
    df['datetime_str'] = df['YEAR'].astype(str) + '-' + \
                         df['MONTH'].astype(str).str.zfill(2) + '-' + \
                         df['DAY'].astype(str).str.zfill(2) + ' ' + \
                         df['TIMEHR'] + ':' + \
                         df['TIMEMIN'] + ' ' + \
                         df['AMPM']
    
    # Convert the datetime string to a datetime object
    df['DATETIME'] = pd.to_datetime(df['datetime_str'], format='%Y-%m-%d %I:%M %p', errors='coerce')
    return df.drop(columns=['datetime_str'])

pd.set_option('display.max_columns', None)
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, 'Railroad_Incidents', 'Dataset.csv')
df_railroad = pd.read_csv(data_path, delimiter=',', low_memory=False)

df_railroad = drop_dummy_columns(df_railroad)
df_railroad = drop_redudant_columns(df_railroad)
df_railroad = drop_sparse_columns(df_railroad, threshold=SPARSENESS_THRESHOLD)
if NEW_DATA_ONLY:
    df_railroad = drop_old_entries(df_railroad)
df_railroad = df_railroad.drop_duplicates()
df_railroad = merge_narration(df_railroad)
df_railroad = format_columns(df_railroad)
df_railroad=filter_measure_errors(df_railroad)
df_railroad=create_datetime_column(df_railroad)

dest_path = os.path.join(current_dir, 'Railroad_Incidents', 'CleanedDataset.csv')
df_railroad.to_csv(dest_path, sep=',', index=False)
