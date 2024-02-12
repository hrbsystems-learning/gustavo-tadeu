# This code will do the same thing as the previous code, but instead of hard-coding the api-key, 
# it will get it from the environment variable MY_SNOV_API_KEY.
# You need to make sure that you have set this environment variable in your system before running the code.

import requests
import os

# Get the API key from the environment variable
api_key = os.environ.get("MY_SNOV_API_KEY")
endpoint = "https://api.snov.io/v1/add-name-to-list"
params = {
"listId": 123,
"email": "john.doe@example.com",
"firstName": "John",
"lastName": "Doe",
"position": "Software Developer",
"source": "LinkedIn"
}

# Make the POST request and get the response
response = requests.post(endpoint, data=params, headers={"Authorization": api_key})

# Check if the request was successful
if response.status_code == 200:
    # Parse the response as JSON
    data = response.json()
    # Print the status and the message
    print(f"Status: {data['status']}")
    print(f"Message: {data['message']}")
else:
    # Print the status code and the error message
    print(f"Request failed with status code {response.status_code}")
    print(response.text)

