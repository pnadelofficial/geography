import os
import time
import pandas as pd
import numpy as np

geography_folder = "/Users/selenawallace/Documents/geography/"
# replace this with paths

class convert_pdf:
    def __init__(self, basin_code):
        self.basin_code = basin_code
        # Replace BCODE below with the BCODE
        self.input_excel = f"{geography_folder}data/status/excel/{self.basin_code}.csv"
        self.output_pdf = f"{geography_folder}data/status/pdf/{self.basin_code}.csv"

    def create_pdf_sheet(self):
        # Read BCODE_excel sheet
        df_excel = pd.read_csv(self.input_excel)
        
        # Select only specific columns with desired headers
        df_excel = df_excel.loc[:, ["BCODE", "Basin_Name", "start_date", "end_date"]]

        # Initialize an empty DataFrame for the result
        df_result = pd.DataFrame(columns=["BCODE", "basin", "key", "set_date", "over_one_thousand", "start_date", "end_date", "start_count", "stop_count", "total_count", "file_name", "finished"])

        # Populate the "key" column with values starting from 1
        df_result["key"] = range(1, len(df_excel) + 1)

        # Populate other columns with values from df_excel
        df_result["BCODE"] = df_excel["BCODE"]
        df_result["basin"] = df_excel["Basin_Name"]
        df_result["start_date"] = df_excel["start_date"]
        df_result["end_date"] = df_excel["end_date"]

        # Initialize an empty DataFrame to store repeated rows
        repeated_df = pd.DataFrame(columns=df_result.columns)

        # Repeat each row 10 times and append to the result DataFrame
        for _, row in df_result.iterrows():
            repeated_rows = pd.concat([pd.DataFrame(row).transpose()] * 2, ignore_index=True)
            repeated_df = pd.concat([repeated_df, repeated_rows], ignore_index=True)

        # Add "set_date" column with desired values
        set_date_values = np.concatenate(([1], np.zeros(1)))  # Generates [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        repeated_df["set_date"] = np.tile(set_date_values, len(df_result))
            
        # Add "start_count" column with desired values
        start_count_values = np.arange(1, 1001, 500)  # Generates [1, 501]
        repeated_df["start_count"] = np.tile(start_count_values, len(df_result))

        # Add "stop_count" column with desired values
        stop_count_values = np.arange(500, 1001, 500)  # Generates [500, 1000]
        repeated_df["stop_count"] = np.tile(stop_count_values, len(df_result))


        # Concatenate the repeated DataFrame with df_result
        df_result = pd.concat([repeated_df], ignore_index=True)

        # Convert "start_date" and "end_date" columns to the desired date format
        df_result["start_date"] = pd.to_datetime(df_result["start_date"]).dt.strftime('%m/%d/%Y')
        df_result["end_date"] = pd.to_datetime(df_result["end_date"]).dt.strftime('%m/%d/%Y')

        # Write the result to BCODE_pdf and add index
        df_result.to_csv(self.output_pdf, index=True, index_label="index")

    def convert(self, basin_code):
        self.__init__(basin_code)
        if os.path.isfile(self.output_pdf):
            print(basin_code, " pdf status file exists")
            pass
        else:
            print(f"need to create pdf status sheet")
            if os.path.isfile(self.input_excel):
                print(f"converting excel status sheet for {basin_code} to pdf")
                self.create_pdf_sheet()
                time.sleep(2)     
                if os.path.isfile(self.output_pdf):
                    print(f"converted {basin_code} pdf status sheet")
                else:
                    print(f"could not convert {basin_code} pdf status sheet")
            else:
                print(f"excel status sheet for {basin_code} could not be found")

        # one more problem - there are a bunch of blank rows?? 
        # I can always figure out why and fix that bug, or...
        # can maybe say ~where start_date is null, delete that row and all the ones after it

#to call this, paste
'''
basin_code = 'tigr'
pdf_conversion = convert_pdf(basin_code)
pdf_conversion.convert(basin_code)
'''