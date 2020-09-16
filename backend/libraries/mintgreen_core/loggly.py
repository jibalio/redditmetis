import requests

LOGGLY_API = "<loggly-url>"

def send_post(data):
    url = LOGGLY_API
    headers = {'Content-type': 'application/json'}
    x = requests.post(url, json = data, headers=headers)
    print(x.status_code)