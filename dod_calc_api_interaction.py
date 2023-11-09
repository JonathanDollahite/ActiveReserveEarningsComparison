import requests 

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
# tax rate URI: https://myarmybenefits.us.army.mil/DoD-Calculator-API/calculator/CalculateTaxRate/single/29796  
# BAS URI: https://www.dfas.mil/MilitaryMembers/payentitlements/Pay-Tables/bas/ 
# continuation pay URI: https://myarmybenefits.us.army.mil/DoD-Calculator-API/calculator/GetConfigurationSettings/2
# pay table growth rate and career progression URI: https://myarmybenefits.us.army.mil/DoD-Calculator-API/calculator/GetMilitaryPayCalculatorSettings/2

