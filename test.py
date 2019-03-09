import json


def gen_dect(src_addr, obj_list):
    for obj in obj_list:
        src_addr['name'] = obj
        data_list.append(src_addr)
    return data_list


def gen_json_data(src_addr, obj_list, key):
    data = {}
    data[key] = gen_dect(src_addr, obj_list)
    return json.dumps(data)


def multi_dest(src_addr, obj_list):
    data_list = []
    for obj in obj_list:
        src_addr['name'] = obj
        data_list.append(src_addr)
        src_addr = {}
    return json.dumps(data_list)


if __name__ == '__main__':
    obj_list = ['a', 'b', 'c']
    data_list = []
    src_addr = {}
    print(gen_json_data(src_addr, obj_list, key='srcaddr'))
    srcintf = multi_dest(src_addr, obj_list)
    dstintf = multi_dest(src_addr, obj_list)
    srcaddr = multi_dest(src_addr, obj_list)
    dstaddr = multi_dest(src_addr, obj_list)

    payload = {'json':
        {
            'srcintf': srcintf,
            'dstintf': dstintf,
            'srcaddr': srcaddr,
            'dstaddr': dstaddr,
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
            'service': [
                {
                    'name': 'service'
                }
            ],
            'comments': 'comments'
        }
    }
    print(payload)
