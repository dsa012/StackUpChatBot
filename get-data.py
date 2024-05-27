import json
import requests

url = 'https://stackuphelpcentre.zendesk.com/api/v2/help_center/en-us/articles?per_page=100'

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    with open('response.json', 'w') as file:
        json.dump(data, file, indent=4)
    print('Response saved to response.json successfully.')
else:
    print(f'Error: {response.status_code} - {response.reason}')
