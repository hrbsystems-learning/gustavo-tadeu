# before executing this script you must to get this 2 info below from your snov account data:
#   your client_id
#   your client_secret
# and create 2 environment variables to receive this 2 values:
# SNOV_CLIENT_ID
# SNOV_SECRET
# having this 2 sensitive info no explicitly coded in the python script is a known good security practice

# imports
import requests
import json
import os
import time


# functions definitions
def access_token_manager():
    """
    this is a closure. Returns a function that is always capable of getting a valid snov api access token  
    """
    saved_access_token = None
    latest_token_obtained_time = None
    client_id = os.getenv('SNOV_CLIENT_ID') # avoid to have sensitive info hardcoded
    client_secret = os.getenv('SNOV_CLIENT_SECRET') # avoid to have sensitive info hasdcoded
    
    def get_new_token():
        nonlocal saved_access_token          # nonlocal => uses the saved_access_token defined above 
        nonlocal latest_token_obtained_time  # nonlocal => uses the token_obtained_time defined above
        params = {
            'grant_type':'client_credentials', 
            'client_id': client_id,
            'client_secret': client_secret
        }
        res = requests.post('https://api.snov.io/v1/oauth/access_token', data=params)
        res_text = res.text.encode('ascii', 'ignore')
        saved_access_token = json.loads(res_text)['access_token']
        latest_token_obtained_time = time.time()

        return saved_access_token

    def get_access_token():
        nonlocal saved_access_token
        nonlocal latest_token_obtained_time
        now = time.time()
        # Check if access_token is None or it has been more than 3600s - 60s since the token was previouslly obtained
        if saved_access_token is None or latest_token_obtained_time is None or (now - latest_token_obtained_time) >= 3600 - 60:
            return get_new_token()
        else:
            return saved_access_token

    return get_access_token


def call_snov_get_domain_search(token):
    params = {
        'access_token': token,
        'domain': 'octagon.com',
        'type': 'all',
        'limit': 100,
        'lastId': 0,
        'positions[]': ['Software Developer', 'QA']
    }
    res = requests.get('https://api.snov.io/v2/domain-emails-with-info', params=params)
    return json.loads(res.text)


def call_snov_get_email_count(token):
    params = {'access_token': token,
              'domain': 'octagon.com'
              }
    res = requests.post('https://api.snov.io/v1/get-domain-emails-count', data=params)
    return json.loads(res.text)


# Begin the program

# Create a new token manager
valid_access_token_genarator = access_token_manager()

resp_domain_search = call_snov_get_domain_search(valid_access_token_genarator())
print(f'domain search exemple call - response: {resp_domain_search}')

resp_email_count = call_snov_get_email_count(valid_access_token_genarator())
print(f'Email count example call - response: {resp_email_count}')
