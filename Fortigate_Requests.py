import FortigateApi
import json
import pyfortiapi

res = {'element': []}

Fortigate_device = FortigateApi.Fortigate("83.206.181.241:20443", "root", "NXO", "testtest123")
i = 1
result = json.loads(Fortigate_device.GetFwIPpool())
print(result['results'])
for interface in result['results']:
    print("IP Pool " + str(i) + " : " + interface['name'] + " " + interface['startip'] + " " + interface['endip'] + " ")
    i = i + 1
