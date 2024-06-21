import requests


url = 'https://my.easyweek.io/api/public/v2/bookings'
myobj = {'somekey': 'somevalue'}
headers = {'Authorization': 'Bearer secret_dAhA2bSsDULrbJ1EPfxFSfIsEI7ys20ngHD34cVBuKs',
           'Workspace': 'test50'}
json = {
  "reserved_on": "2024-06-21T10:00:00Z",
  "location_uuid": "41bc234f-2716-4395-983f-13b81f42bcea",
  "service_uuid": "53e80956-b6a3-4d3a-acd1-dcaf89e5b102",
  "customer_phone": "491621234567",
  "customer_first_name": "Name",
}

x = requests.post(url, json = json, headers=headers)

print(x.text)

#curl -i -X GET   https://my.easyweek.io/api/public/v2/locations/41bc234f-2716-4395-983f-13b81f42bcea/services -H 'Authorization: Bearer secret_dAhA2bSsDULrbJ1EPfxFSfIsEI7ys20ngHD34cVBuKs'   -H 'Workspace: test50'

#curl -i -X GET   https://my.easyweek.io/api/public/v2/locations -H 'Authorization: Bearer secret_dAhA2bSsDULrbJ1EPfxFSfIsEI7ys20ngHD34cVBuKs'   -H 'Workspace: test50'
