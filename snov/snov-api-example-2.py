# before testing or executing this script you must to get his 2 info below from your snov account data:
#   your client_id
#   your client_secret
# and replace respective parameters values in function get_access_token() function definition


import requests
import json


def get_access_token():
    params = {
        'grant_type': 'client_credentials',
        'client_id': 'c57a0459f6t141659ea75cccb393c111',  # replace this field value with your client_id
        'client_secret': '77cbf92b71553e85ce3bfd505214f40b'  # replace this field value with your client_secret
    }
    res = requests.post('https://api.snov.io/v1/oauth/access_token', data=params)
    res_text = res.text.encode('ascii', 'ignore')
    return json.loads(res_text)['access_token']


def get_domain_search(token):
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


def get_email_count(token):
    params = {'access_token': token,
              'domain': 'octagon.com'
              }
    res = requests.post('https://api.snov.io/v1/get-domain-emails-count', data=params)
    return json.loads(res.text)


# Begin the program

access_token = get_access_token()
resp_domain_search = get_domain_search(access_token)
print(f'domain search exemple call - response: {resp_domain_search}')

resp_email_count = get_email_count(access_token)
print(f'Email count example call - response: {resp_email_count}')
