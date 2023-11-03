from requests import get


def get_latest_lib_url():
    response = get('https://api.github.com/repos/yushijinhun/authlib-injector/releases/latest')
    for asset in response.json()['assets']:
        if asset['name'].endswith('.jar'):
            return asset['browser_download_url']
