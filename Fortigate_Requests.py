import FortigateApi
import json
import ipcalc
import six
import pyfortiapi

"""res = {'element': []}

Fortigate_device = FortigateApi.Fortigate("83.206.181.241:20443", "root", "NXO", "testtest123")
i = 1
result = json.loads(Fortigate_device.GetFwIPpool())
print(result['results'])
for interface in result['results']:
    print("IP Pool " + str(i) + " : " + interface['name'] + " " + interface['startip'] + " " + interface['endip'] + " ")
    i = i + 1"""

###############################################

# Create VDOM with param Vdom_Name

Vdom_name = 'Vdom_3'
Firewall_v2 = FortigateApi.Fortigate("192.168.19.141", "root", "PFE", "pfepfe")
result = json.loads(Firewall_v2.GetVdom())
vdom_list = []
for vdom in result['results']:
    vdom_list.append(vdom['name'])
if Vdom_name in vdom_list:
    print("Vdom Exist")
else:
    Firewall_v2.AddVdom(Vdom_name)
    print("Vdom " + Vdom_name + " created successfully")

# Create and associate Interfaces to VDOM with params

Vlan_name = 'Vlan400'
Aggregate_Lan = "AGG"
Vlan_Id = "400"
Adr_IP = "172.16.32.254/24"
Allowed_Access = "ping ssh https"
result = json.loads(Firewall_v2.GetInterface())
intefaces_list = []
for interface in result:
    intefaces_list.append(interface['name'])
if Vlan_name in intefaces_list:
    print("Vlan " + Vlan_name + " exist")
else:
    print("creating interface")
    Firewall_v2.AddVlanInterface(Vlan_name, Aggregate_Lan, Vlan_Id, Adr_IP, Vdom_name, Allowed_Access)

# Create Local Admin

SystemAdmin_list = []
Vdom_Admin = "Vdom_3_Admin"
password = 'admin'
result = json.loads(Firewall_v2.GetSystemAdmin())
print(result['results'])
for SysAdmin in result['results']:
    SystemAdmin_list.append(SysAdmin['name'])
if Vdom_Admin in SystemAdmin_list:
    print("Admin account already exist")
else:
    Firewall_v2.AddSystemAdmin(Vdom_Admin, password, profile='prof_admin', remote_auth='disable')

# Creating Policies objects

Firewall_v2_noprev = FortigateApi.Fortigate("192.168.19.141", Vdom_name, "test", "test")

IPPool = "185.33.66.99"
IPPool_Name = Vdom_name + "_IPPool"
Lan_Network = str(ipcalc.Network(Adr_IP).network()) + "/" + str(ipcalc.Network(Adr_IP).subnet())
ippool_list = []
print(Lan_Network)

## IPOOl ( no vdom )

"""result = json.loads(Firewall_v2_noprev.GetFwIPpool())
for ip in result['results']:
    ippool_list.append(ip['name'])
if IPPool in ippool_list:
    print("IPPool Exist")
else:
    Firewall_v2_noprev.AddFwIPpool(IPPool_Name, IPPool, IPPool)
    print("IP Pool Created successfully")
print(Firewall_v2_noprev.GetFwIPpool())

## Adresse Objects
# print(Firewall_v2.GetFwAddress())"""
