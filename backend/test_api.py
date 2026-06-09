import urllib.request
import urllib.parse
import json
import sys

base_url = "http://127.0.0.1:8000/api/v1"

def req(method, path, data=None, token=None):
    url = base_url + path
    headers = {}
    if data is not None:
        data = json.dumps(data).encode('utf-8')
        headers['Content-Type'] = 'application/json'
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            return response.status, json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())
    except Exception as e:
        return 0, str(e)

# 1. Login (we need freelancer credentials)
# Assuming a default user exists from previous scripts? Let's just create one or use a common one.
# Wait, I don't know the password. I can just bypass auth by using a direct DB query, 
# but the easiest way is to print the last few lines of the uvicorn log.
