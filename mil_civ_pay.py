import pandas as pd
import plotly.express as px
import requests

mil_pay_df = pd.read_excel('mil_pay.xlsx')
stop_index = mil_pay_df['Military Pay'].last_valid_index()
years, n = mil_pay_df['Calendar Year'], 20
mil_pay_df['Post Mil Retirement Pay'] = [0] * len(years)
if stop_index is not None: mil_pay_df.loc[stop_index + 1:stop_index + n, 'Post Mil Retirement Pay'] = 123000
selected_columns = ['Military Pay', 'Bonus & Payments', 'BRS Pension', 'Service Member TSP Payout', "Gov't TSP Payout", 'Post Mil Retirement Pay']

fig = px.bar(mil_pay_df, x='Calendar Year', y=selected_columns, title='Mil Pay', barmode='stack')
#fig.show()

# Replace 'your_uri_here' with the actual URI you want to request.
base_pay_uri = 'https://myarmybenefits.us.army.mil/DoD-Calculator-API/calculator/CalculateBasicPay/0/O-1'
headers = {"User-Agent": "python/3.11"}

try:
    response = requests.get(base_pay_uri, headers=headers)
    if response.status_code == 200:
        base_pay = response.text
        print(f'Value stored as base_pay: {base_pay}')
    else:
        print(f'Failed to retrieve data. Status code: {response.status_code}')
except requests.exceptions.RequestException as e:
    print(f'An error occurred: {e}')

# base pay URI: https://myarmybenefits.us.army.mil/DoD-Calculator-API/calculator/CalculateBasicPay/0/O-1
# BAH URI: https://myarmybenefits.us.army.mil/DoD-Calculator-API/calculator/CalculateBAH/1/O-1/32508
# tax rate: https://myarmybenefits.us.army.mil/DoD-Calculator-API/calculator/CalculateTaxRate/single/29796  
# BAS URI: https://www.dfas.mil/MilitaryMembers/payentitlements/Pay-Tables/bas/ 
