import requests

# URL for the local Flask API
url = 'http://127.0.0.1:5000/analyze_transaction'

# Sample transaction data for testing
data = {
    'amount': 500,
    'location_match': 1,
    'time_of_day': 14
}

# Send a POST request to the API
response = requests.post(url, json=data)

# Print the API's response
if response.status_code == 200:
    print('Response:', response.json())
else:
    print('Error:', response.status_code, response.text)
