import constants.prog as prog
import os
import json

data_storage_dir = prog.data_storage_dir
prog_reg_file = prog.reg_file
prog_reg_filepath = prog.reg_filepath

def ensure_file_exists():
    if not os.path.exists(data_storage_dir):
        os.makedirs(data_storage_dir)

    if not os.path.exists(prog_reg_filepath):
        with open(prog_reg_filepath, 'w') as file:
            json.dump({}, file)

def get_prog_register():
    ensure_file_exists()
    with open(prog_reg_filepath, 'r') as file:
        return json.load(file)

def get_prog_register_key(key):
    data = get_prog_register()
    if key not in data:
        return None
    return data.get(key)

def update_prog_register(key, value):
    data = get_prog_register()
    data[key] = value
    with open(prog_reg_filepath, 'w') as file:
        json.dump(data, file, indent=4)