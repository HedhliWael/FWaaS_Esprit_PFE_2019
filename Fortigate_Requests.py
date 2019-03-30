import FortigateApi
import json
import ipcalc
import six
import pyfortiapi

###############################################
FGT_Root = "192.168.136.129"
FGT_Vdom = "192.168.1.83"
# vdom_name = 'Vdom_3'

"""Firewall_v2 = FortigateApi.Fortigate(FGT_Root, "root", "admin", "admin")
Firewall_v2_noprev = FortigateApi.Fortigate(FGT_Root, vdom_name, "admin", "admin")
Firewall_v2_api2 = pyfortiapi.FortiGate(ipaddr=FGT_Root, username="admin", password="admin", vdom=vdom_name)"""


# Create VDOM with param Vdom_Name

def c_vdom(vdom_name, Firewall_v2):
    msg = ""
    res = json.loads(Firewall_v2.GetVdom())
    vdom_list = []
    for vdom in res['results']:
        vdom_list.append(vdom['name'])
    if vdom_name in vdom_list:
        msg = "Vdom Exist ! "
    else:
        Firewall_v2.AddVdom(vdom_name)
        msg = "Vdom " + str(vdom_name) + " created successfully"
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
#ippool_name = vdom_name + "_IPPool"


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
def c_policy(Firewall_v2_noprev, srcintf, dstintf, srcaddr, dstaddr, services, nat, ipool,
             poolname, comment):
    Firewall_v2_noprev.AddFwPolicy(srcintf=srcintf, dstintf=dstintf, srcaddr=srcaddr, nat=nat,
                                   ippool=ipool,
                                   poolname=poolname, dstaddr=dstaddr, service=services,
                                   comments=comment)
    return "Policy Created successfully"


def c_policy_m(Firewall_v2_noprev, srcintf, dstintf, srcaddr, dstaddr, services, nat, ipool,
               poolname, comment):
    Firewall_v2_noprev.AddFwPolicy_m(srcintf=srcintf, dstintf=dstintf, srcaddr=srcaddr, nat=nat,
                                     ippool=ipool,
                                     poolname=poolname, dstaddr=dstaddr, service=services,
                                     comments=comment)
    return "Policy Created successfully"


# Creating Routes

def c_route(selector, Firewall_v2_noprev, destination, gw, interface, comment):
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
    if selector == 1:
        for rt in json_resultat['results']:
            route_list.append(rt['dst'])
        print(route_list)
        if destination in route_list:
            msg = "Route Exist , skipping creating"
        else:
            Firewall_v2_noprev.AddRouterStatic(destination, interface, str(gw_r), comment)
            msg = "Route " + destination + " created successfully"

        return msg
    else:
        for rt in json_resultat['results']:
            route_list.append(rt['dst'])
        print(route_list)
        if destination in route_list:
            msg = "Route Exist , skipping creating"
        else:
            Firewall_v2_noprev.AddRouterStatic(destination, interface, str(gw), comment)
            msg = "Route " + destination + " created successfully"

        return msg


def gen_dec(obj_list):
    data_list = []
    src_addr = {}
    for obj in obj_list:
        src_addr["name"] = obj
        data_list.append(src_addr)
        src_addr = {}
    return data_list


def g_intrf_list(Firewall_v2_noprev):
    json_resultat = json.loads(Firewall_v2_noprev.GetInterface())
    interf_list = []
    for interface in json_resultat:
        interf_list.append(interface['name'])
    return interf_list


def g_intrf_list_labeled(vdom_name):
    fw = FortigateApi.Fortigate(FGT_Root, vdom_name, "admin", "admin")
    json_resultat = json.loads(fw.GetInterface())
    interf_list = []
    for interface in json_resultat:
        interf_list.append(str(vdom_name) + "*" + str(interface['name']))
    return interf_list


def g_objects_list_labeled(adr):
    fw = pyfortiapi.FortiGate(ipaddr=FGT_Root, username="admin", password="admin", vdom=str(adr))
    # json_resultat = json.loads(fw.get_firewall_address())
    json_resultat = fw.get_firewall_address()
    interf_list = []
    for interface in json_resultat:
        interf_list.append(str(adr) + "*" + str(interface['name']))
    return interf_list


def g_srv_list_labeled(adr):
    fw = pyfortiapi.FortiGate(ipaddr=FGT_Root, username="admin", password="admin", vdom=str(adr))
    # json_resultat = json.loads(fw.get_firewall_address())
    json_resultat = fw.get_firewall_service()
    interf_list = []
    for interface in json_resultat:
        interf_list.append(str(adr) + "*" + str(interface['name']))
    return interf_list


def g_srv_list(Firewall_v2_api2):
    json_resultat = Firewall_v2_api2.get_service_group()
    srv_list = []
    for srv in json_resultat:
        srv_list.append(srv['name'])
    return srv_list


def g_adr_list(Firewall_v2_api2):
    json_resultat = Firewall_v2_api2.get_firewall_address()
    adr_list = []
    for adr in json_resultat:
        adr_list.append(adr['name'])
    return adr_list


def g_ippool_list(Firewall_v2_noprev):
    ippool_list = []
    json_resultat = json.loads(Firewall_v2_noprev.GetFwIPpool())
    for ip in json_resultat['results']:
        ippool_list.append(ip['name'])
    return ippool_list


def g_ippool_list_labeled(adr):
    fw = FortigateApi.Fortigate(FGT_Root, adr, "admin", "admin")
    json_resultat = json.loads(fw.GetFwIPpool())
    print(json_resultat)
    interf_list = []
    for interface in json_resultat['results']:
        interf_list.append(str(adr) + "*" + str(interface['name']))
    return interf_list


def g_vdom_list(Firewall_v2_noprev):
    vdom_list = []
    json_resultat = json.loads(Firewall_v2_noprev.GetVdom())
    for vd in json_resultat['results']:
        vdom_list.append(vd['name'])
    return vdom_list


def g_policy_id(fw_vdom, id):
    return fw_vdom.GetFwPolicyID(id=str(id))


"""def g_all_vdom_intef():
    FW = FortigateApi.Fortigate(FGT_Root, "root", "admin", "admin")
    vdom_list = g_vdom_list(FW)
    all_interf_list = []
    for vdom in vdom_list:
        Firewall_v2_noprev = FortigateApi.Fortigate(FGT_Root, vdom, "admin", "admin")
        vdom_interf_list = g_intrf_list_labeled(Firewall_v2_noprev)
        all_interf_list = all_interf_list + vdom_interf_list
    return all_interf_list"""


def g_all_vdom_intef():
    FW = FortigateApi.Fortigate("192.168.136.129", "root", "admin", "admin")
    vdom_list = g_vdom_list(FW)
    all_interf_list = []
    for vdom in vdom_list:
        vdom_interf_list = g_intrf_list_labeled(vdom)
        all_interf_list = all_interf_list + vdom_interf_list
    return all_interf_list


def g_all_vdoms_adr():
    FW = FortigateApi.Fortigate("192.168.136.129", "root", "admin", "admin")
    vdom_list = g_vdom_list(FW)
    all_adr_list = []
    for vdom in vdom_list:
        vdom_adr_list = g_objects_list_labeled(vdom)
        all_adr_list = all_adr_list + vdom_adr_list
    return all_adr_list


def g_all_vdoms_srv():
    FW = FortigateApi.Fortigate("192.168.136.129", "root", "admin", "admin")
    vdom_list = g_vdom_list(FW)
    all_adr_list = []
    for vdom in vdom_list:
        vdom_adr_list = g_srv_list_labeled(vdom)
        all_adr_list = all_adr_list + vdom_adr_list
    return all_adr_list


def g_all_vdoms_ippool():
    FW = FortigateApi.Fortigate("192.168.136.129", "root", "admin", "admin")
    vdom_list = g_vdom_list(FW)
    all_adr_list = []
    for vdom in vdom_list:
        vdom_adr_list = g_ippool_list_labeled(vdom)
        all_adr_list = all_adr_list + vdom_adr_list
    return all_adr_list


if __name__ == '__main__':
    vdom_name = "root"
    Firewall_v2_noprev = FortigateApi.Fortigate(FGT_Root, vdom_name, "admin", "admin")
    Firewall_v2_api2 = pyfortiapi.FortiGate(ipaddr=FGT_Root, username="admin", password="admin", vdom=vdom_name)
    list_intrf = g_ippool_list_labeled(vdom_name)
    print("all interfaces : " + str(list_intrf))
