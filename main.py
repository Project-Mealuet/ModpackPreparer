from configparser import ConfigParser
from json import dump
from logging import getLogger, basicConfig, INFO
from os.path import exists, join

from api.curseforge_api import get_modpack_meta
from client.prep_client import prep_client
from server.prep_server import prep_server

if __name__ == '__main__':
    basicConfig()

    config = ConfigParser()
    log = getLogger()
    log.setLevel(INFO)

    if not exists('config.ini'):
        log.info('config.ini created. ')
        config.read_dict({
            'general': {
                'curseforge_id': '681792',
                'curseforge_api_key': 'Enter curseforge api key here',
            },
            'client': {
                'enable': 'yes',
                'game_path': '/root/mc'
            },
            'server': {
                'enable': 'yes',
                'server_path': '/root/mc',
                'memory_limit': '18'
            },
            'ssh': {
                'enable': 'yes',
                'host': 'localhost',
                'port': '22',
                'username': 'user',
                'key_path': '/path/to/key',
                'root': '/root/path'
            }
        })
        with open('config.ini', 'w') as config_file:
            config.write(config_file)
    else:
        log.info('config.ini was read. ')
        config.read('config.ini', encoding='UTF-8')
        server_meta = get_modpack_meta(str(config['general']['curseforge_id']), config['general']['curseforge_api_key'])
        with open(join(config['server']['server_path'], 'server_meta.json'), 'w', encoding='UTF-8') as server_meta_file:
            dump(server_meta, server_meta_file, ensure_ascii=False, indent=4)
        if config['client']['enable'].strip().lower() == 'yes':
            prep_client(
                config['client']['game_path'],
                server_meta['mod_loader'],
                server_meta['game_version']
            )
        if config['client']['enable'].strip().lower() == 'yes':
            prep_server(
                config['server']['server_path'],
                server_meta['game_version'],
                server_meta['mod_loader'],
                config['server']['memory_limit'],
                server_meta['name']
            )
