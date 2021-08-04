import json
import os
from constants import path_to_data, all_region_defaults_file


def load_json(json_filename: str):
    if os.path.isfile(json_filename):
        if json_filename.endswith('.json'):
            with open(json_filename, 'r') as f:
                return json.load(f)
        else:
            raise ValueError(f'{json_filename} is not a JSON file')
    else:
        raise FileNotFoundError(f'Could not find {json_filename}')


def get_region_filename(region):
    return f'{region.name}.json'


def get_relative_path(path, filename):
    return f'{path}/{filename}'


def load_region_json(region):
    region_filename = get_region_filename(region)
    path = get_relative_path(path_to_data, region_filename)
    return load_json(path)


def load_all_region_json():
    path = get_relative_path(path_to_data, all_region_defaults_file)
    return load_json(path)


def get_enum(enum_class, enum_name):
    return enum_class[enum_name]


def get_key_from_value(search_dict, value):
    keys = list(search_dict.keys())
    values = list(search_dict.values())
    if len(values) != len(list(dict.fromkeys(values))):
        raise ValueError(f'{search_dict} does not contain unique values!')
    else:
        return keys[values.index(value)]
