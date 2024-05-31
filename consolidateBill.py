import pandas as pd
import json

# Read JSON data from file
with open('costmanagement_outout_val_1.json', 'r') as file:
    data = json.load(file)

# Convert JSON data to DataFrame
df = pd.DataFrame(data)

# Clean the 'Amount' column
# df['Amount'] = df['Amount'].str.replace('USD', '').str.replace('(', '-').str.replace(')', '').str.replace(',', '').str.replace(' ', '').str.strip()

# Convert 'Amount' to float
df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
# df['Amount'] *=df['Amount'].apply(lambda x:-1 if str(x).startswith("-") else 1)
# df['Amount'] = pd.to_numeric(df['Amount'].str.replace('[^\d.-]', ''), errors='coerce')
# df.loc[df['Amount'].str.startswith('-'),'Amount'] *=-1

df.to_excel("consolidateBill/convertedAmount.xlsx")
# Group by 'solution_provide', 'service_name', and 'location' and sum the 'Amount'
grouped_df = df.groupby(['service_name', 'location'])['Amount'].sum().reset_index()


# Group by 'service_name' and sum the 'Amount'
service_name_df = df.groupby(['service_name'])['Amount'].sum().reset_index()

# Write the results to Excel files
output_file_grouped = "consolidateBill/sum_amount_grouped.xlsx"
output_file_solution_provide = "consolidateBill/sum_amount_solution_provide.xlsx"
output_file_service_name = "consolidateBill/sum_amount_service_name.xlsx"

grouped_df.to_excel(output_file_grouped, index=False)
service_name_df.to_excel(output_file_service_name, index=False)

print("Data written to", output_file_grouped)
print("Data written to", output_file_solution_provide)
print("Data written to", output_file_service_name)
