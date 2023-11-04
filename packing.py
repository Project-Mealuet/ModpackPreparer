from configparser import ConfigParser
from json import load
from os import system, chdir
from os.path import join
from shutil import copytree

GIT_ROOT = r'E:\mealuet-serverpacks'

config = ConfigParser()
config.read('config.ini', encoding='UTF-8')
packing_path = config['server']['server_path']
with open(join(packing_path, 'server_meta.json'), 'r', encoding='UTF-8') as server_meta_file:
    server_meta = load(server_meta_file)
dst_name = (server_meta['name']
            .replace(' ', '_')
            .replace('/', '_')
            .replace('\\', '_')
            .replace(':', '_')
            .replace('*', '_')
            .replace('?', '_')
            .replace('"', '_')
            .replace('<', '_')
            .replace('>', '_')
            .replace('|', '_'))
dist_path = join(GIT_ROOT, dst_name)

copytree(packing_path, dist_path)
chdir(GIT_ROOT)
system('git pull')
system('git add .')
system(f'git commit -m "Update {server_meta['name']} serverpack. "')
system('git push origin main')
