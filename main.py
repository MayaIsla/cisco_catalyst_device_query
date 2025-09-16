
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

api_uri = "https://tenant.saasit.com/api/odata/businessobject/CIs"
iv_auth_header = {'Authorization': ivnt_api__Key}


network_device_json = requests.get(device_auth_uri , headers = catalyst_headers, verify=False)

for i in network_device_json.json()['response']:
    device_host_name = i['hostname']
    device_serial_number = i['serialNumber']
    device_platformId = i['platformId']
    device_managementIpAddress = i['managementIpAddress']
    
    ivnt_get_phone_exists = "https://tenant.saasit.com/api/odata/businessobject/CIs?$search=" + device_serial_number
    
    if ivnt_get_phone_exists.status_code == 204: #204 no content - means switch doesn't exist
      body_response = str('{"MACAddress": ' + '"' + device_host_name + '","IPAddress":' + '"' +  device_managementIpAddress + '","SerialNumber":' + '"' + device_serial_number + '"' +"}")
      update_CI = requests.post(url= api_uri,  data= body_response, headers=iv_auth_header)

