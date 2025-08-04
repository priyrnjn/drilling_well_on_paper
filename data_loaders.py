import os
import pandas as pd

user = os.getlogin()
if user.lower() == "priyr":
    file_path = r"C:\Users\priyr\OneDrive - Oil and Natural Gas Corporation Limited\1. Next Wells\2. Benchmarking\DDKG1 - DDR.xlsm"
elif user.lower() == "priyaranjan":
    file_path = r"C:\Users\Priyaranjan\OneDrive - Oil and Natural Gas Corporation Limited\1. Next Wells\2. Benchmarking\DDKG1 - DDR.xlsm"
else:
    raise Exception("Unknown user, file path not set")

df_rates = pd.read_excel(file_path, sheet_name='Sheet2', engine='openpyxl')
rates = df_rates.iloc[:, 7:10]
rates = rates[~rates['Unnamed: 7'].isna()]
rates.columns = ['Sr No', 'Activity', 'Activity_Rate'] 
def rate(activity):
    row = rates[rates['Activity'] == activity]
    if not row.empty:
        return row['Activity_Rate'].iloc[0]
    else:
        print(f"Activity '{activity}' not found in rates.")
        return None  # or raise an error
activity_rates = dict(zip(rates['Activity'], rates['Activity_Rate']))