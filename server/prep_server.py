from base64 import b64decode
from logging import getLogger
from os.path import exists, join

from jproperties import Properties

from jre_config import check_lib_exist, download_lib, add_jre_args
from utils.server_icon import server_icon


def _modify_properties(
        server_path: str,
        game_version: str
):
    server_properties = Properties()
    server_properties_path = join(server_path, 'server.properties')
    if exists(server_properties_path):
        with open(server_properties_path, 'rb') as file:
            server_properties.load(file, encoding='UTF-8')
    server_properties['max-players'] = '5'
    server_properties['motd'] = 'Server maintained by Mealuet, dedicated to YOU. '
    server_properties['pvp'] = 'false'
    server_properties['online-mode'] = 'true'
    server_properties['allow-flight'] = 'true'
    server_properties['enable-query'] = 'true'
    server_properties['query.port'] = '25585'
    if game_version == '1.12.2':
        server_properties['difficulty'] = '3'
    else:
        server_properties['difficulty'] = 'hard'
    with open(server_properties_path, 'wb') as file:
        server_properties.store(file, encoding='UTF-8')


def _allow_eula(
        server_path: str
):
    with open(join(server_path, 'eula.txt'), 'w') as file:
        file.write('eula=true')


def _config_server_icon(
        server_path: str
):
    with open(join(server_path, 'server-icon.png'), 'wb') as image_file:
        image_file.write(b64decode(server_icon))


def prep_server(
        server_path: str,
        game_version: str,
        memory_limit: str
):
    log = getLogger('server')

    _modify_properties(server_path, game_version)
    log.info('server properties modified. ')
    _allow_eula(server_path)
    log.info('eula allowed. ')
    if not check_lib_exist(server_path):
        log.warning('no authlib-injector found. ')
        download_lib(server_path)
        log.info('authlib-injector downloaded. ')
    add_jre_args(server_path, memory_limit)
    log.info('jre args added. ')
    _config_server_icon(server_path)
    log.info('server-icon added. ')
