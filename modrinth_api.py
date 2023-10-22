from requests import get


def _get_from_modrinth(
        path: str,
        params: dict = None
):
    if params is None:
        params = {}
    response = get(
        url='https://api.modrinth.com/v2' + path,
        headers={
            'Content-Type': 'application/json'
        },
        json=params
    )
    return response.json()


def get_latest_file_url(
        project_id: str,
        loaders: list[str],
        game_versions: list[str]
):
    response = _get_from_modrinth(f'/project/{project_id}/version')
    for version in response:
        if (loaders[0].lower() in version['loaders']) and (game_versions[0] in version['game_versions']):
            return version['files'][0]['url']
