import pandas as pd
import plotly.express as px
import numpy as np
import os

SPARSENESS_THRESHOLD = 0.99 # All columns where there are (SPARSENESS_THRESHOLD * 100)% n/a values will be dropped
NEW_DATA_ONLY = True # If True, all data entries preceding 2011 will be dropped
DROP_0_COORD = True # If True, all data entries with coordinates 0,0 will be dropped

def drop_redudant_columns(df):
    """Drops columns that convey info already present in other existing columns."""

    df = df.drop(columns=["IYR", "IYR2", "IYR3", "YEAR", "IMO", "IMO2", "IMO3",
                          "CASINJRR", "CASKLDRR"], axis=1, errors='ignore')
    df.rename(columns={'YEAR4': 'YEAR'}, inplace=True)
    df.rename(columns={'Longitud': 'Longitude'}, inplace=True)
    return df


def drop_dummy_columns(df):
    """Drops dummy columns."""
    return df.drop(columns=["DUMMY1", "DUMMY2", "DUMMY3", "DUMMY4", "DUMMY5", "DUMMY6", 
                            "ADJUNCT1", "ADJUNCT2", "ADJUNCT3", "SSB1", "SSB2"], axis=1, errors='ignore')
    

def drop_sparse_columns(df, threshold):
    """Drops all columns with a null entry ratio greater than a given threshold."""

    # Calculate the null rate for each column
    null_rates = df.isna().mean()
    # Filter column names where the null rate exceeds the threshold
    high_null_columns = null_rates[null_rates > threshold].index.tolist()
    return df.drop(columns=high_null_columns, axis=1, errors='ignore')


def drop_old_entries(df):
    """Drop all entries preceding 2011."""

    count_old = df[df['YEAR'] < 2011].shape[0]
    count_new = df[df['YEAR'] >= 2011].shape[0]
    print(f"Deleting {count_old} records from 2001 or earlier, {count_new} records remain.")
    return df[df['YEAR'] >= 2011]


def drop_error_entries(df):
    """Drops all entries where the coordinates are mistakinly either in the ocean or outside of USA territory."""

    # Define approximate USA boundary (continental only)
    min_latitude = 24.396308   # Southernmost point (Hawaii excluded)
    max_latitude = 49   # Northernmost point
    min_longitude = -125.0     # Westernmost point
    max_longitude = -66.93457  # Easternmost point

    # Define approximate Alaska boundaries
    alaska_min_latitude = 51.2097    # Southernmost point in Alaska
    alaska_max_latitude = 71.5388    # Northernmost point in Alaska
    alaska_min_longitude = -179.1489 # Westernmost point in Alaska
    alaska_max_longitude = -129.9795 # Easternmost point in Alaska

    # Filter rows within the USA boundary
    df = df[
        (
            (df['Latitude'] >= min_latitude) & 
            (df['Latitude'] <= max_latitude) &
            (df['Longitude'] >= min_longitude) & 
            (df['Longitude'] <= max_longitude)
        ) |
        (
            (df['Latitude'] >= alaska_min_latitude) & 
            (df['Latitude'] <= alaska_max_latitude) &
            (df['Longitude'] >= alaska_min_longitude) & 
            (df['Longitude'] <= alaska_max_longitude)
        ) |
        (
            (df['Latitude'] == 0) &
            (df['Longitude'] == 0)
        )
    ]

    # Drop remaining error entries
    df = df[~((df['Latitude'] == 40.194395) & (df['Longitude'] == -71.795028))]
    df = df[~((df['Latitude'] == 40.450002) & (df['Longitude'] == -73.550081))]
    df = df[~((df['Latitude'] == 45.349) & (df['Longitude'] == -67.06))]
    df = df[~((df['Latitude'] == 44.4493) & (df['Longitude'] == -81.67709))]
    df = df[~((df['Latitude'] == 42.191607) & (df['Longitude'] == -83.075516))]
    df = df[~((df['Latitude'] == 42.160202) & (df['Longitude'] == -83.082612))]
    df = df[
            ~(
                (df['Latitude'] >= 31.758696 - 0.0001) & 
                (df['Latitude'] <= 31.758696 + 0.0001) & 
                (df['Longitude'] >= -116.500855 - 0.0001) & 
                (df['Longitude'] <= -116.500855 + 0.0001)
            )
        ]    
    df = df[~((df['Latitude'] == 32.35343) & (df['Longitude'] == -116.31232))]
    return df


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
    """
    Filters entries of incidents with the same ID that happened at the same time,
    keeping only the most recent entry (assumed to be the last in the current index order).
    """
    # def get_best_entry(group):
    #     non_null_ratio = group.notnull().mean(axis=1)
    #     return group.loc[non_null_ratio.idxmax()]

    def get_best_entry(group):
        return group.iloc[-1]  # Keep the last entry in the group
    
    grouped = df.groupby(['INCDTNO', 'YEAR', 'MONTH', 'DAY', 'TIMEHR', 'TIMEMIN'])
    return grouped.apply(get_best_entry).reset_index(drop=True)
    

def format_columns(df):
    """Formats column values in easier to manage types."""
    
    df['PASSTRN'] = df['PASSTRN'].replace({'Y': True, 'N': False}).fillna(False)
    df['LOADED1'] = df['LOADED1'].replace({'Y': True, 'N': False})
    df['LOADED2'] = df['LOADED2'].replace({'Y': True, 'N': False})
    df['EQATT'] = df['EQATT'].replace({'Y': True, 'N': False})
    return df


def replace_alcohol_drug_nan(df):
    df['DRUG'] = df['DRUG'].fillna(-1)
    df['ALCOHOL'] = df['ALCOHOL'].fillna(-1)
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


def replace_null_coordinates(df):
    """
    Replaces null values in the 'Latitude' and 'Longitude' columns with 0.
    """
    df['Latitude'] = df['Latitude'].fillna(0)
    df['Longitude'] = df['Longitude'].fillna(0)
    return df


def drop_0_coord_entries(df):
    """
    Drops all entries where coordinates are 0,0.
    """
    return df[(df['Latitude'] != 0) & (df['Longitude'] != 0)].copy()


def sanity_checks(df):
    """
    Drops all entries where entries do not satisfy sanity checks
    """
    #temp 1 outlier max temp, lower temps look okay
    max_temp = 150
    old_size = df.shape[0]
    count_temp= df[df['TEMP'] < max_temp].shape[0]
    print(f"Deleting {old_size - count_temp} based on temp")
    df = df[df['TEMP']< max_temp]

    return df
    #speed, totkld, totinjured, did check, looks fine
    #damage costs




pd.set_option('display.max_columns', None)
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, 'Railroad_Incidents', 'Dataset.csv')
df_railroad = pd.read_csv(data_path, delimiter=',', low_memory=False)

df_railroad = drop_dummy_columns(df_railroad)
df_railroad = drop_redudant_columns(df_railroad)
df_railroad = drop_sparse_columns(df_railroad, threshold=SPARSENESS_THRESHOLD)
df_railroad=replace_null_coordinates(df_railroad)
df_railroad=drop_error_entries(df_railroad)
if NEW_DATA_ONLY:
    df_railroad = drop_old_entries(df_railroad)
df_railroad = df_railroad.drop_duplicates()
df_railroad = merge_narration(df_railroad)
df_railroad = format_columns(df_railroad)
df_railroad=filter_measure_errors(df_railroad)
df_railroad=create_datetime_column(df_railroad)
if DROP_0_COORD:
    df_railroad=drop_0_coord_entries(df_railroad)
df_railroad = sanity_checks(df_railroad)    
df_railroad = replace_alcohol_drug_nan(df_railroad)
dest_path = os.path.join(current_dir, 'Railroad_Incidents', 'CleanedDataset.csv')
df_railroad.to_csv(dest_path, sep=',', index=False)




