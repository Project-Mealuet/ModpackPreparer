from os import makedirs
from os.path import join

from api.modrinth_api import download_mod


def download_bluemap(
        server_path: str,
        loader: str,
        game_version: str
):
    download_mod(join(server_path, 'mods'), loader, game_version, 'swbUV1cr')


def config_bluemap(
        server_path: str
):
    config_path = join(server_path, 'config/bluemap')
    makedirs(config_path, True)
    with open(join(config_path, 'core.conf'), 'w', encoding='UTF-8') as config_file:
        config_file.write('accept-download: true\nrender-thread-count: -2')
