import yaml
import glob

roms = []

def initialize():
    config = get_config()
    roms_dir = config['roms_directory']

    rom_files = glob.glob(roms_dir + '/*.zip')
    for file in rom_files:
        roms.append(file)

def get_config():
    with open('config.yml', 'r') as file:
        return yaml.safe_load(file)