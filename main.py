
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

api_uri = "https://tenant.saasit.com/api/odata/businessobject/CI_ivnt_infrastructures" #Cannot use the CI business object due to misconfiguration of the newer tenant. -_-
iv_auth_header = {'Authorization': ivnt_api__Key}


network_device_json = requests.get(device_auth_uri , headers = catalyst_headers, verify=False)

for i in network_device_json.json()['response']:
    device_host_name = i['hostname']
    device_serial_number = i['serialNumber']
    device_platformId = i['platformId']
    device_managementIpAddress = i['managementIpAddress']
    print(device_host_name + " " + device_serial_number + " " + device_platformId + " " + device_managementIpAddress)
    
    
    ivnt_get_phone_exists = "https://tenant.saasit.com/api/odata/businessobject/CI__ivnt_infrastructures?$search=" + device_serial_number
    ivnt_get_phone = requests.get(url = ivnt_get_phone_exists, headers=iv_auth_header)
    print(update_CI.text)
    
    if ivnt_get_phone.status_code == 204: #204 no content - means switch doesn't exist
      body_response = str('{"IPAddress":' + '"' +  device_managementIpAddress + '","Status": "Production",' + '"ivnt_AssetSubtype": "Network Switch - 24p' +  '","CIType": "ivnt_Infrastructure' + '","SerialNumber":' + '"' + device_serial_number +  '","Name":' + '"' + device_host_name + '"' + "}")
      # FullyQualifiedDomainName is "Name" + "DomainName" Setup as a business rule.
      # Update body to add discovered data (Discovered manufacturer, model), Status, FQDN, IP, Mac Address (Verify with Catalyst API documentation).
      update_CI = requests.post(url= api_uri,  data= body_response, headers=iv_auth_header)
      print(update_CI.text)
        
    else:
      if ivnt_get_phone.status_code == 200: #Phone exists, update record with RecID.
          request_iv_get_recID_text = ivnt_get_phone.text
          json_RecID = json.loads(request_iv_get_recID_text)

          for i in json_RecID['value']:
              ivnt_ci_RecId = (i['RecId'])
              

          ivnt_ci_mod_url = "https://tenant.saasit.com/api/odata/businessobject/CI__ivnt_infrastructures('" + ivnt_ci_RecId + "')"
          body_response = str('{"IPAddress":' + '"' +  device_managementIpAddress + '","SerialNumber":' + '"' + device_serial_number + '","Name":' + '"' + device_host_name + '"' + "}")
          update_existing_CI = requests.put(url=ivnt_ci_mod_url, data= body_response, headers=iv_auth_header)
          print(update_existing_CI.text)
          
    else: 
        print("No 200 or 204 error please look at transcript.") #error handles, log will show failed json.
        ivnt_get_phone = "https://tenant.saasit.com/api/odata/businessobject/CI__ivnt_infrastructures?$search=" + device_serial_number
        request_ivnt_phone_exists = requests.get(url = ivnt_get_phone, headers=iv_auth_header)
        text_CSV =  request_ivnt_phone_exists.text
        with open("C:/dir/to/error/logging/error_log.csv","w") as file:
            file.write(text_CSV + "\n")

