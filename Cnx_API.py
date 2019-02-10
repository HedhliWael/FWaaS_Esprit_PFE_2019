import pyfortiapi

group = "Acces_Full_FTP"
res = {'element': []}

device = pyfortiapi.FortiGate(ipaddr="83.206.181.241:20443", username="NXO", password="testtest123")

req = device.get_address_group(group)

for m in req[0]['member']:
    res['element'].append(m['name'])
print(res)
