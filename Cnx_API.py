import pyfortiapi
import FortigateApi
import json


def g_policy_elements(FGT):
    policy = {}
    policies = []
    json_resultat = json.loads(FGT.GetFwPolicyID())
    for element in json_resultat['results']:
        policy["srcintf"] = element["srcintf"][0]['name']
        policy["dstintf"] = element["srcintf"][0]['name']
        policy["srcaddr"] = element["srcaddr"][0]['name']
        policy["dstaddr"] = element["dstaddr"][0]['name']
        policy["service"] = element["service"][0]['name']
        if element["poolname"]:
            policy["poolname"] = element["poolname"][0]['name']
        else:
            policy["poolname"] = ''
        # print(element["srcintf"][0]['name'])
        policies.append(policy)
        policy = {}
    return policies


if __name__ == '__main__':
    group = "Acces_Full_FTP"
    res = []
    FGT_Root = "192.168.136.129"
    FGT_Vdom = "192.168.1.83"

    vdom_name = 'root'

    device = pyfortiapi.FortiGate(ipaddr="83.206.181.241:20443", username="NXO", password="testtest123")
    Firewall_v2_api2 = pyfortiapi.FortiGate(ipaddr=FGT_Root, username="admin", password="admin", vdom="Vdom_V1")
    fortigate = FortigateApi.Fortigate(FGT_Root, 'Vdom_V1', "PFE", "pfepfe")

    req = Firewall_v2_api2.get_firewall_address()

    for m in req:
        res.append(m['name'])

    # print(fortigate.GetFwPolicyID())
    print('test---------------------------------------------')
    fortigate = FortigateApi.Fortigate(FGT_Root, 'Vdom_V1', "PFE", "pfepfe")
    for pol in g_policy_elements(fortigate):
        print(pol.get('srcintf'))
