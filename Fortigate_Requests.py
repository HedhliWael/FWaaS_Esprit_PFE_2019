import FortigateApi
import json
import ipcalc
import six
import pyfortiapi

###############################################
FGT_Root = "192.168.136.129"
FGT_Vdom = "192.168.1.83"

vdom_name = 'Vdom_3'
Firewall_v2 = FortigateApi.Fortigate(FGT_Root, "root", "admin", "admin")
Firewall_v2_noprev = FortigateApi.Fortigate(FGT_Root, vdom_name, "admin", "admin")


# Create VDOM with param Vdom_Name

def c_vdom(vdom_name, Firewall_v2):
    msg = ""
    res = json.loads(Firewall_v2.GetVdom())
    vdom_list = []
    for vdom in res['results']:
        vdom_list.append(vdom['name'])
    if vdom_name in vdom_list:
        msq = "Vdom Exist ! "
    else:
        Firewall_v2.AddVdom(vdom_name)
        msq = "Vdom " + str(vdom_name) + " created successfully"
    return msg


# Create and associate Interfaces to VDOM with params

def c_intrf_vlan(vdom_name, Firewall_v2, vlan, intrf_physique, vlan_id, ip,
                 allowed_access):
    msg = ""
    json_resultat = json.loads(Firewall_v2.GetInterface())
    intfr_list = []
    for interface in json_resultat:
        intfr_list.append(interface['name'])
    if vlan in intfr_list:
        msg = "Vlan " + vlan + " exist, skipping creation"
    else:
        msg = "creating interface " + vlan
        Firewall_v2.AddVlanInterface(vlan, intrf_physique, vlan_id, ip, vdom_name, allowed_access)
    return msg


# Create Local Admin
def c_admin(vdom_name, Firewall_v2, admin_name, password):
    msg = ""
    admin_list = []
    json_resultat = json.loads(Firewall_v2.GetSystemAdmin())
    for SysAdmin in json_resultat['results']:
        admin_list.append(SysAdmin['name'])
    if admin_name in admin_list:
        msg = "Admin account already exist , Skipping Creation"
    else:
        Firewall_v2.AddSystemAdmin(admin_name, password, profile='prof_admin', remote_auth='disable')
        msg = "Admin Created successfully"
    return msg


# Creating Policies objects


## IPOOl
ippool_name = vdom_name + "_IPPool"


def c_ippool(Firewall_v2_noprev, ippool, ippool_name, vdom_name):
    msg = ""
    ippool_list = []
    # ippool_name = vdom_name + "_IPPool"
    json_resultat = json.loads(Firewall_v2_noprev.GetFwIPpool())
    for ip in json_resultat['results']:
        ippool_list.append(ip['name'])
    if ippool in ippool_list:
        msg = "IPPool Exist " + ippool + ", Skipping "
    else:
        Firewall_v2_noprev.AddFwIPpool(ippool_name, ippool, ippool)
        msg = "IP Pool Created successfully"
    return msg


## Adresse Objects
def c_adr_obj(Firewall_v2_noprev, ip, object_name):
    json_resultat = json.loads(Firewall_v2_noprev.GetFwAddress())

    adrs_list = []
    msg = ""
    object_adresse = str(ipcalc.Network(ip).network()) + "/" + str(ipcalc.Network(ip).subnet())
    for adr in json_resultat['results']:
        adrs_list.append(adr['name'])
    if object_name in adrs_list:
        msg = "Object exists , skipping creation"
    else:
        Firewall_v2_noprev.AddFwAddress(object_name, object_adresse)
        msg = "Object " + object_name + " Created successfully"
    return msg


# Creating Policy LAN to Wan
def c_policy(Firewall_v2_noprev, srcintf, dstintf, srcaddr, nat, ipool, poolname, comment):
    Firewall_v2_noprev.AddFwPolicy(srcintf=srcintf, dstintf=dstintf, srcaddr=srcaddr, nat=nat,
                                   ippool=ipool,
                                   poolname=poolname,
                                   comments=comment)
    return "Policy Created successfully"


# Creating Routes

def c_route(Firewall_v2_noprev, destination, gw, interface, comment):
    msg = ""
    route_list = []
    print('------------------------------------------------')
    gw_r = ipcalc.Network(gw).host_last()
    print("route for " + destination)
    print("GW param " + str(gw))
    print("Real GW " + str(gw_r))
    print("interface de sortie " + interface)

    json_resultat = json.loads(Firewall_v2_noprev.GetRouterStaticID())
    print(json_resultat)
    for rt in json_resultat['results']:
        route_list.append(rt['dst'])
    print(route_list)
    if destination in route_list:
        msg = "Route Exist , skipping creating"
    else:
        Firewall_v2_noprev.AddRouterStatic(destination, interface, str(gw_r), comment)
        msg = "Route " + destination + " created successfully"

    return msg


if __name__ == '__main__':
    vdom_name = "Veolia"
    Firewall_v2_noprev = FortigateApi.Fortigate(FGT_Root, vdom_name, "admin", "admin")
    print(c_route(Firewall_v2_noprev, '10.0.0.0/8', '100.255.255.200/24', 'Veolia_LAN', "test"))
