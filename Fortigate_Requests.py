import FortigateApi
import json
import ipcalc
import six
import pyfortiapi

###############################################
FGT_Root = "192.168.136.129"
FGT_Vdom = "192.168.1.83"

# Create VDOM with param Vdom_Name

Vdom_name = 'Vdom_3'
Firewall_v2 = FortigateApi.Fortigate(FGT_Root, "root", "PFE", "pfepfe")
result = json.loads(Firewall_v2.GetVdom())
vdom_list = []
for vdom in result['results']:
    vdom_list.append(vdom['name'])
if Vdom_name in vdom_list:
    print("Vdom Exist ! ")
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
    print("Vlan " + Vlan_name + " exist, skipping creation")
else:
    print("creating interface")
    Firewall_v2.AddVlanInterface(Vlan_name, Aggregate_Lan, Vlan_Id, Adr_IP, Vdom_name, Allowed_Access)

# Create Local Admin

SystemAdmin_list = []
Vdom_Admin = "Vdom_3_Admin"
password = 'admin'
result = json.loads(Firewall_v2.GetSystemAdmin())
for SysAdmin in result['results']:
    SystemAdmin_list.append(SysAdmin['name'])
if Vdom_Admin in SystemAdmin_list:
    print("Admin account already exist , Skipping Creation")
else:
    Firewall_v2.AddSystemAdmin(Vdom_Admin, password, profile='prof_admin', remote_auth='disable')

# Creating Policies objects

Firewall_v2_noprev = FortigateApi.Fortigate(FGT_Root, Vdom_name, "admin", "admin")

IPPool = "185.33.66.99"
IPPool_Name = Vdom_name + "_IPPool"
Lan_Network = str(ipcalc.Network(Adr_IP).network()) + "/" + str(ipcalc.Network(Adr_IP).subnet())
ippool_list = []
Lan_Network_Object = Lan_Network + "_LAN"

## IPOOl

result = json.loads(Firewall_v2_noprev.GetFwIPpool())
for ip in result['results']:
    ippool_list.append(ip['name'])
if IPPool in ippool_list:
    print("IPPool Exist " + IPPool + ", Skipping ")
else:
    Firewall_v2_noprev.AddFwIPpool(IPPool_Name, IPPool, IPPool)
    print("IP Pool Created successfully")

## Adresse Objects

result = json.loads(Firewall_v2_noprev.GetFwAddress())
Adr_list = []
for adrs in result['results']:
    Adr_list.append(adrs['name'])
if Lan_Network_Object in Adr_list:
    print("Object exists , skipping creation")
else:
    Firewall_v2_noprev.AddFwAddress(Lan_Network_Object, Lan_Network)
    print("Object " + Lan_Network_Object + " Created successfully")

# Creating Policy LAN to Wan

Firewall_v2_noprev.AddFwPolicy(srcintf='Vlan400', dstintf='Vlan800', srcaddr=Lan_Network_Object, nat='enable',
                               ippool='enable',
                               poolname=IPPool_Name,
                               comments='auto-generated')
print("Policy Created successfully")

# Creating Routes
rfc_1918_1 = "10.0.0.0 255.0.0.0"
rfc_1918_2 = "172.16.0.0 255.240.0.0"
rfc_1918_3 = "192.168.0.0 255.255.0"
Gw_Lan = "20.20.20.254"
Gw_Wan = "40.40.40.254"

route_list = []
result = json.loads(Firewall_v2_noprev.GetRouterStaticID())
for rt in result['results']:
    route_list.append(rt['dst'])
if (rfc_1918_1 in route_list) and (rfc_1918_2 in route_list) and (rfc_1918_3 in route_list):
    print("Route Exist , skipping creating")
else:
    Firewall_v2_noprev.AddRouterStatic(rfc_1918_1, 'Vlan400', Gw_Lan, comment='RFC 10/8 to LAN')
    Firewall_v2_noprev.AddRouterStatic(rfc_1918_2, 'Vlan400', Gw_Lan, comment='RFC 172.16/12 to LAN')
    Firewall_v2_noprev.AddRouterStatic(rfc_1918_3, 'Vlan400', Gw_Lan, comment='RFC 192.168/16 to LAN')
    Firewall_v2_noprev.AddRouterStatic("0.0.0.0 0.0.0.0", 'Vlan800', Gw_Wan, comment='Default Route via Wan interface')
    print("Routes created successfully")
