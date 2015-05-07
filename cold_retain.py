__author__ = 'alexander'

import json

def cold_retain(object, list_with_vars):
    data_dict = {}
    for var in list_with_vars:
       data_dict[var] = object.__dict__[var]
    with open('ColdRetain.json', 'w') as json_file:
        json_file.write(json.dumps(data_dict))

def cold_retain_load(object):
    with open('ColdRetain.json', 'r') as json_file:
        json_data = json.loads(json_file.read())
    return json_data

