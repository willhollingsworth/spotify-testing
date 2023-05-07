import os
import requests
import json


def print_dict_keys(input_dict, keys=''):
    # nicer printing of dictionaries
    if len(keys) < 1: # if no keys specified then print all
        keys = input_dict.keys()
    for key in keys:
        if isinstance(key, str):
            print(key, ':', input_dict[key], end=', ')
        elif isinstance(key, list):
            if len(key) == 2:
                print(key[0], key[1], ':',
                      input_dict[key[0]][key[1]], end=', ')
    print()
    return


def download_data(url, headers='', overwrite=0, debug=0, type='json'):
    cache_folder = 'cache/'
    if not os.path.exists(cache_folder):
        os.mkdir(cache_folder)
    striped_characters = ':/\|?"'
    processed_url = url
    for char in striped_characters:
        processed_url = processed_url.replace(char, '_')

    full_path = cache_folder + processed_url
    if type == 'json':
        full_path += '.json'
    if type == 'html':
        full_path += '.html'
    if os.path.exists(full_path) and not overwrite:
        with open(full_path, 'r') as f:
            if type == 'json':
                r = json.load(f)
            else:
                r = f
    else:
        r = requests.get(url, headers=headers)
        if type == 'json':
            r = r.json()
        if debug:
            print(r['tracks'].keys())
        if 'data' in r:
            r = r['data']
        with open(full_path, 'w') as f:
            if type == 'json':
                f.write(json.dumps(r, indent=4))
            else:
                f.write(r)
    return r


def load_credentials(service):
    valid_services = ['spotify', 'last_fm']
    # add check for credentials file, if false create a blank one in the right format with appropriate error msg
    if not service in valid_services:
        raise Exception('chosen service: ', service,
                        ' is not a valid service, only the following are allowed', valid_services)
    '''' load credentials via json'''
    with open('credentials.json', 'r') as r:
        credentials = json.load(r)[service]
    return credentials


def save_to_file(data, filename):
    with open(filename, 'w') as f:
        f.write(data)
