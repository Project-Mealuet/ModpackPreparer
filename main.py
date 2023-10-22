from prep_client import prep_client
from prep_server import prep_server


if __name__ == '__main__':
    choice_type = input('Client or Server? ')
    if choice_type == 'Client':
        game_path = input('Game Path: ')
        loaders = [input('Mod Loader: ')]
        game_versions = [input('Game Version: ')]
        prep_client(game_path, loaders, game_versions)
    elif choice_type == 'Server':
        server_path = input('Server Path: ')
        game_versions = [input('Game Version: ')]
        prep_server(server_path, game_versions)
