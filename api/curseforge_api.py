from re import fullmatch

from requests import get


def _get_from_curseforge(
        route: str,
        api_key: str
):
    return get(
        url=f'https://api.curseforge.com{route}',
        headers={
            'Accept': 'application/json',
            'x-api-key': api_key
        }
    ).json()


def _get_mod_info(
        mod_id: str,
        api_key: str
):
    return _get_from_curseforge(f'/v1/mods/{mod_id}', api_key)


def get_modpack_meta(
        modpack_id: str,
        api_key: str
):
    raw_data = _get_mod_info(modpack_id, api_key)
    game_version = None
    mod_loader = None
    for latest_file in raw_data['data']['latestFiles']:
        if 'gameVersions' in latest_file:
            game_versions = latest_file['gameVersions']
            for version in game_versions:
                if game_version is None:
                    if fullmatch(r'1\.[1-9][0-9]?(\.[1-9][0-9]?)?', version):
                        game_version = version
                if mod_loader is None:
                    if version.lower() in ['fabric', 'forge', 'quilt', 'neoforge']:
                        mod_loader = version.lower()
        if (game_version is not None) and (mod_loader is not None):
            break
    return {
        'name': raw_data['data']['name'],
        'logo': raw_data['data']['logo']['url'],
        'game_version': game_version,
        'mod_loader': mod_loader
    }
