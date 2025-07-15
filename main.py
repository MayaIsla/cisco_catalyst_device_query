
import requests
import json
from requests.auth import HTTPBasicAuth
import urllib3
urllib3.disable_warnings()

auth_URI = 'https://server.local/dna/system/api/v1/auth/token'

USERNAME = '' #will probably make this base64 for auth code
PASSWORD = ''

response = requests.post(auth_URI , auth=HTTPBasicAuth(USERNAME, PASSWORD), verify=False)
auth_key_text = response.text

parsed_auth_key_json = json.loads(auth_key_text)
parsed_auth_key_text = parsed_auth_key_json["Token"]

catalyst_headers = {'X-Auth-Token': parsed_auth_key_text}
device_auth_uri = 'https://server.local/dna/intent/api/v1/network-device'

network_device_json = requests.get(device_auth_uri , headers = catalyst_headers, verify=False)

for i in network_device_json.json()['response']:
    print(i['hostname'] + " - " + i['serialNumber'] + " - " + i['platformId'] + " - " + i['managementIpAddress'])
