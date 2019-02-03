import FortigateApi
import json
import pyfortiapi

res = {'element': []}

Fortigate_device = FortigateApi.Fortigate("83.206.181.241:20443", "root", "NXO", "testtest123")

result = json.loads(Fortigate_device.GetInterface())

for interface in result:
    print(interface['name'])
