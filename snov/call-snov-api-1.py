import requests

api_key = "your_api_key_here"
endpoint = "https://api.snov.io/v1/get-domain-emails-with-info"
params = {
"domain": "datacamp.com", # The domain to search for
"type": "all", # The type of emails to return (all, personal, or generic)
"limit": 10, # The maximum number of emails to return
"lastId": 0 # The ID of the last email to start from (0 for the first page)
}

response = requests.get(endpoint, params=params, headers={"Authorization": api_key})

# Check if the request was successful
if response.status_code == 200:
    # Parse the response as JSON
    data = response.json()
    # Print the number of emails found
    print(f"Found {data['result']['count']} emails for {params['domain']}")
    # Loop through the emails and print their information
    for email in data['result']['emails']:
        print(f"Email: {email['email']}")
        print(f"First name: {email['firstName']}")
        print(f"Last name: {email['lastName']}")
        print(f"Position: {email['position']}")
        print(f"Source: {email['sourcePage']}")
        print("-" * 20)
else:
    # Print the status code and the error message
    print(f"Request failed with status code {response.status_code}")
    print(response.text)
