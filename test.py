import json
import re


def param_extract(param):
    list_map = []
    dect = {}
    split1 = param.split()
    for int_map in split1:
        split2 = re.split('->|\*', int_map)
        dect['vdom_v1'] = split2[0]
        dect['interface_v1'] = split2[1]
        dect['vdom_v2'] = split2[2]
        dect['interface_v2'] = split2[3]
        list_map.append(dect)
        dect = {}
    return list_map


def gen_dect(src_addr, obj_list):
    for obj in obj_list:
        src_addr['name'] = obj
        data_list.append(src_addr)
    return data_list


def gen_json_data(src_addr, obj_list, key):
    data = {}
    data[key] = gen_dect(src_addr, obj_list)
    return json.dumps(data)


def mutli_element(obj_list):
    data_list = []
    src_addr = {}
    for obj in obj_list:
        src_addr['name'] = obj
        data_list.append(src_addr)
        src_addr = {}
    return json.dumps(data_list)


if __name__ == '__main__':
    obj_list = ['a', 'b', 'c']
    obj_list2 = ['d', 'e', 'f']
    flist = obj_list + obj_list2
    mot = "test*after"
    print(str(mot.split('*')[1]))
    print(flist)
    data_list = []
    src_addr = {}
    # print(gen_json_data(src_addr, obj_list, key='srcaddr'))
    srcintf = mutli_element(obj_list)
    dstintf = mutli_element(obj_list)
    srcaddr = mutli_element(obj_list)
    dstaddr = mutli_element(obj_list)
    srvc = mutli_element(obj_list)
    payload = {'json':
        {
            'srcintf': str(srcintf),
            'dstintf': str(dstintf),
            'srcaddr': str(srcaddr),
            'dstaddr': str(dstaddr),
            'action': 'permit',
            'schedule': 'schedule',
            'nat': 'nat',
            'status': 'status',
            'nat': 'nat',
            'ippool': 'ippool',
            'traffic-shaper': 'traffic_shaper',
            'traffic-shaper-reverse': 'traffic_shaper_reverse',
            'poolname': [
                {
                    'name': 'poolname'
                }
            ],
            'service': srvc,
            'comments': 'comments'
        }
    }
    print(payload)
param = 'Vdom_V1*V1_Vlan200->Vdom_V2*V2_Vlan300 Vdom_V1*V1_vlan100->Vdom_V2*V2_Vlan301'
print(param_extract(param))
