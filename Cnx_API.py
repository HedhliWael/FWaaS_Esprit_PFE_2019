import pyfortiapi

group = "Acces_Full_FTP"
res = []
FGT_Root = "192.168.136.129"
FGT_Vdom = "192.168.1.83"

vdom_name = 'Veolia'

device = pyfortiapi.FortiGate(ipaddr="83.206.181.241:20443", username="NXO", password="testtest123")
Firewall_v2_api2 = pyfortiapi.FortiGate(ipaddr=FGT_Root, username="admin", password="admin", vdom=vdom_name)

req = Firewall_v2_api2.get_service_group()

for m in req:
    res.append(m['name'])

print(res)
