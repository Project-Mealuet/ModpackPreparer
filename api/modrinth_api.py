from os.path import join, exists
from urllib.parse import unquote

from requests import get
from wget import download


def _get_from_modrinth(
        route: str,
        params=None
):
    if params is None:
        params = {}
    return get(
        url=f'https://api.modrinth.com/v2{route}',
        headers={
            'Content-Type': 'application/json'
        },
        json=params
    ).json()


def _get_latest_file_url(
        project_id: str,
        loader: str,
        game_version: str
):
    response = _get_from_modrinth(f'/project/{project_id}/version')
    for version in response:
        if (loader.lower() in version['loaders']) and (game_version in version['game_versions']):
            return unquote(version['files'][0]['url'])
    return None


def download_mod(
        mods_path: str,
        loader: str,
        game_version: str,
        project_id: str
):
    file_url = _get_latest_file_url(
        project_id,
        loader,
        game_version
    )
    if file_url is None:
        return False

    file_name = file_url.strip().split('/')[-1]
    if not exists(join(mods_path, file_name)):
        download(file_url, join(mods_path, file_name))
    return True
