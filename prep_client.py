from logging import getLogger
from os.path import exists
from os.path import join

from nbtlib import File as NBTFile
from nbtlib import parse_nbt

from mc_options import McOptions
from modrinth_api import download_mod


def _load_server_list(
        game_path: str
):
    servers_dat = NBTFile()
    servers_dat['servers'] = parse_nbt("[{'ip': 'server.mealuet.com','name': 'Mealuet Server'}]")
    servers_dat.save(join(game_path, 'servers.dat'), gzipped=False)


def _load_options(
        game_path: str
):
    options = McOptions()
    if exists(join(game_path, 'options.txt')):
        options.load(join(game_path, 'options.txt'))
    options['lang'] = 'zh_cn'
    options.save(join(game_path, 'options.txt'))


def prep_client(
        game_path: str,
        loader: str,
        game_version: str
):
    log = getLogger('client')

    mods_path = join(game_path, 'mods')
    if download_mod(mods_path, loader, game_version, 'PWERr14M'):
        log.info('i18n downloaded. ')
    else:
        log.error('no matched i18n. ')
    if game_version != '1.12.2':
        if download_mod(mods_path, loader, game_version, 'WMDesFsZ'):
            log.info('imblocker downloaded. ')
        else:
            log.error('no matched imblocker')
    else:
        log.critical('imblocker is not eligible for 1.12.2! ')
    _load_server_list(game_path)
    log.info('server list added. ')
    _load_options(game_path)
    log.info('game language switched to zh_cn. ')
