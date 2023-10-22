from os.path import exists
from os.path import join

from nbtlib import File as NBTFile
from nbtlib import parse_nbt

from mc_options import McOptions
from skin_src_config import download_mod, add_skin_src


def _load_server_list(
        game_path: str
):
    servers_dat = NBTFile()
    servers_dat['servers'] = parse_nbt("[{'ip': 'server.mealuet.online','name': 'Mealuet Server'}]")
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
        loaders: list[str],
        game_versions: list[str]
):
    mods_path = join(game_path, 'mods')
    download_mod(mods_path, loaders, game_versions, 'idMHQ4n2')
    print('Client: CML downloaded. ')
    download_mod(mods_path, loaders, game_versions, 'PWERr14M')
    print('Client: i18n downloaded. ')
    add_skin_src(game_path)
    print('Client: MealuetSkin added. ')
    _load_server_list(game_path)
    print('Client: Server added. ')
    _load_options(game_path)
    print('Client: Language changed to zh_cn. ')
