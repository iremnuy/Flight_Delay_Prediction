import pandas as pd
import numpy as np

def convert_time_to_float(value):
    """Converts HHMM-style time (e.g., 1359.0) to float (13.59)."""
    if pd.isna(value):
        return np.nan
    value = int(value)
    hours = value // 100
    minutes = value % 100
    return round(hours + minutes / 100, 2)


def data_clean(input_path, output_path):

    df = pd.read_csv(input_path)

    # remove diverted and cancalled rows
    df = df[(df['CANCELLED'] == 0) & (df['DIVERTED'] == 0)] # this implicitly removed all the other null values

    # drop unnecessary and duplicated columns
    """
        'OP_CARRIER', 'OP_UNIQUE_CARRIER', 'OP_CARRIER_AIRLINE_ID' are same,
        'ORIGIN', 'ORIGIN_AIRPORT_ID' are same
        'DEST', 'DEST_AIRPORT_ID' are same
        keep only one of the identical columns, can change which one to keep from the code below
    """

    df = df.drop(columns=['CANCELLED', 'DIVERTED', 'Unnamed: 21', 
                        'OP_CARRIER_AIRLINE_ID', 'OP_UNIQUE_CARRIER', 'ORIGIN_AIRPORT_ID', 'DEST_AIRPORT_ID'])  

    # change time format
    for col in ['DEP_TIME', 'ARR_TIME']:
        if col in df.columns:
            df[col] = df[col].apply(convert_time_to_float)

    # convert binary columns from float to int 
    binary_cols = ['DEP_DEL15', 'ARR_DEL15']
    df[binary_cols] = df[binary_cols].astype('int')

    # add new columns
    df['IS_WEEKEND'] = df['DAY_OF_WEEK'].isin([6, 7]).astype(int)
    df['IS_DELAYED'] = ((df['DEP_DEL15'] == 1) | (df['ARR_DEL15'] == 1)).astype(int)
    df['ROUTE'] = (df['ORIGIN'].astype(str) + '_' + df['DEST'].astype(str))

    df.to_csv(output_path, index=False)


data_clean("data/Jan_2019_2020_ontime.csv", "data/19_20_cleaned_data.csv")