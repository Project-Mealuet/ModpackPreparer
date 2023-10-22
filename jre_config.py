from os.path import exists, join

from requests import get

from github_api import get_latest_lib_url


def check_lib_exist(
        server_path: str
):
    if exists(join(server_path, 'authlib-injector.jar')):
        return True
    return False


def download_lib(
        server_path: str
):
    lib_url = get_latest_lib_url()
    with open(join(server_path, 'authlib-injector.jar'), 'wb') as file:
        file.write(get(lib_url).content)


def add_jre_args(
        server_path: str
):
    with open(join(server_path, 'user_jvm_args.txt'), 'w') as file:
        file.write('-Xms22G -Xmx22G -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 '
                   '-XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch '
                   '-XX:G1NewSizePercent=40 -XX:G1MaxNewSizePercent=50 -XX:G1HeapRegionSize=16M '
                   '-XX:G1ReservePercent=15 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 '
                   '-XX:InitiatingHeapOccupancyPercent=20 -XX:G1MixedGCLiveThresholdPercent=90 '
                   '-XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem '
                   '-XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true '
                   '-javaagent:authlib-injector.jar=https://skin.mealuet.com/api/yggdrasil')
