
#get general info about csv datast 

import pandas as pd

def get_dataset_info(file_path):

    # Load the dataset
    for file in file_path:
        df = pd.read_csv(file)
        #save first 10 rows to csv
        df.head(50).to_csv(f'first_50_rows_{file.split("/")[-1]}', index=False)
        
        # Get general information
        info = {
            "num_rows": df.shape[0],
            "num_columns": df.shape[1],
            "column_names": df.columns.tolist(),
            "data_types": df.dtypes.to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "first_five_rows": df.head().to_dict(orient='records')
        }
        print(info)
    

# Example usage
get_dataset_info(["2/Jan_2020_ontime.csv","2/Jan_2019_ontime.csv"])