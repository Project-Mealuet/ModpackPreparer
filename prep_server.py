from os.path import exists, join

from jproperties import Properties

from jre_config import check_lib_exist, download_lib, add_jre_args


def _modify_properties(
        server_path: str,
        game_versions: list[str]
):
    server_properties = Properties()
    server_properties_path = join(server_path, 'server.properties')
    if exists(server_properties_path):
        with open(server_properties_path, 'rb') as file:
            server_properties.load(file, encoding='UTF-8')
    server_properties['max-players'] = '5'
    server_properties['server-port'] = '80'
    server_properties['motd'] = 'MealuetServer for Minecraft, dedicated to Zack_ZHU'
    server_properties['pvp'] = 'false'
    server_properties['online-mode'] = 'true'
    server_properties['allow-flight'] = 'true'
    if game_versions[0] == '1.12.2':
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


def prep_server(
        server_path: str,
        game_versions: list[str]
):
    _modify_properties(server_path, game_versions)
    print('Server: Properties modified. ')
    _allow_eula(server_path)
    print('Server: EULA allowed. ')
    if not check_lib_exist(server_path):
        print('Server: No authlib-injector found. ')
        download_lib(server_path)
        print('Server: authlib-injector downloaded. ')
    add_jre_args(server_path)
    print('Server: JRE args added. ')
