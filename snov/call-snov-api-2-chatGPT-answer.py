# This code is a chatGPT answer from de prompt below:
# Prompt:
# Please, write a python script that is capable do make a POST HTTP request to snov api.

# This code will send a POST request to the snov api with your api-key and the parameters for adding a prospect to a list.
# If the request is successful, it will return a JSON object with the status and the message.
# If the request fails, it will return the status code and the error message.
# You can find more information and examples of the snov api methods and parameters on their official website https://snov.io/knowledgebase/how-to-use-snov-io-api/.

# my comments from the chatGPT answer:
# the info below, I got from the snov api documentation. 
# The code is correct, but chatGPT doesn't take in account the necessity to get the access-token first of all.


import requests

api_key = "your_api_key_here"
endpoint = "https://api.snov.io/v1/add-name-to-list"
params = {
"listId": 123, # The ID of the list to which you want to add the prospect
"email": "john.doe@example.com", # The email of the prospect
"firstName": "John", # The first name of the prospect
"lastName": "Doe", # The last name of the prospect
"position": "Software Developer", # The position of the prospect
"source": "LinkedIn" # The source of the prospect
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

