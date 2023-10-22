from json import dump as json_dump
from json import load as json_load
from os import listdir, makedirs
from os.path import join, exists
from tomllib import load as toml_load
from zipfile import ZipFile

from requests import get

from modrinth_api import get_latest_file_url


def download_mod(
        mods_path: str,
        loaders: list[str],
        game_versions: list[str],
        project_id: str
):
    file_url = get_latest_file_url(
        project_id,
        loaders,
        game_versions
    )
    file_name = file_url.split('/')[-1]
    with open(join(mods_path, file_name), 'wb') as file:
        file.write(get(file_url).content)


def check_cml_exist(
        mods_path: str,
        game_versions: list[str]
):
    mods_files_names = [file_name for file_name in listdir(mods_path) if file_name.endswith('.jar')]
    if game_versions[0] != '1.12.2':
        for file_name in mods_files_names:
            jar_file = ZipFile(join(mods_path, file_name))
            with jar_file.read('META-INF/mods.toml') as meta_file:
                mod_id = toml_load(meta_file)['mods'][0]['modId']
            if mod_id == 'customskinloader':
                return True
    else:
        for file_name in mods_files_names:
            jar_file = ZipFile(join(mods_path, file_name))
            with jar_file.open('mcmod.info') as meta_file:
                mod_id = json_load(meta_file)[0]['modid']
            if mod_id == 'customskinloader':
                return True
    return False


def add_skin_src(
        game_path: str
):
    if not exists(join(game_path, 'CustomSkinLoader/ExtraList')):
        makedirs(join(game_path, 'CustomSkinLoader/ExtraList'))
    with open(join(game_path, 'CustomSkinLoader/ExtraList/MealuetSkin.json'), 'w') as config_file:
        config = {
            'name': 'MealuetSkin',
            'type': 'CustomSkinAPI',
            'root': 'https://skin.mealuet.com/csl/'
        }
        json_dump(config, config_file)
