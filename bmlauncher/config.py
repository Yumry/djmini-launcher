import yaml
import glob

roms = []
bindings = {}

def initialize():
    config = get_config()
    roms_dir = config['roms_directory']

    rom_files = glob.glob(roms_dir + '/*.zip')
    for file in sorted(rom_files):
        roms.append(file)
    
    for bind_name, value in config['key_bindings'].items():
        bindings[bind_name]=value
    print(bindings)

def get_config():
    with open('config.yml', 'r') as file:
        return yaml.safe_load(file)

def save_config():
    config = get_config()
    config['key_bindings'] = bindings
    with open('config.yml', 'w') as outfile:
        yaml.safe_dump(config, outfile, default_flow_style=False, sort_keys=False)