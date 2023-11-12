from configparser import ConfigParser
from json import load
from os import walk, remove
from os.path import join, relpath, dirname, basename
from zipfile import ZipFile, ZIP_DEFLATED

from paramiko import RSAKey, SSHClient, AutoAddPolicy

config = ConfigParser()
config.read('config.ini', encoding='UTF-8')


def zipdir(directory_to_zip, zip_filename):
    with ZipFile(zip_filename, 'w', ZIP_DEFLATED) as zipf:
        for root, _, files in walk(directory_to_zip):
            for file in files:
                full_path = join(root, file)
                archive_path = join(basename(zip_filename).rsplit('.', 1)[0], relpath(full_path, directory_to_zip))
                zipf.write(full_path, archive_path)


packing_path = config['server']['server_path']
with open(join(packing_path, 'server_meta.json'), 'r', encoding='UTF-8') as server_meta_file:
    server_meta = load(server_meta_file)
packing_name = (server_meta['name']
                .replace(' ', '_')
                .replace('/', '_')
                .replace('\\', '_')
                .replace(':', '_')
                .replace('*', '_')
                .replace('?', '_')
                .replace('"', '_')
                .replace('<', '_')
                .replace('>', '_')
                .replace('|', '_') + '.zip')
print('正在打包serverpack……')
zipdir(packing_path, join(dirname(packing_path), packing_name))

if config['ssh']['enable'].strip().lower() == 'true':
    src_path = join(dirname(packing_path), packing_name)
    dist_path = config['ssh']['root']
    key_file = RSAKey.from_private_key_file(config['ssh']['key_path'])

    ssh_client = SSHClient()
    ssh_client.set_missing_host_key_policy(AutoAddPolicy())
    ssh_client.connect(config['ssh']['host'], int(config['ssh']['port']), config['ssh']['username'], pkey=key_file)

    print('正在上传serverpack……')
    sftp_client = ssh_client.open_sftp()


    def print_progress(transferred, total):
        print(f"已传输： {transferred}/{total} bytes ({transferred / total * 100:.2f}%)")


    sftp_client.put(src_path, join(dist_path, packing_name).replace('\\', '/'), callback=print_progress)
    print('正在解压serverpack……')
    unzip_command = (f'cd {dist_path} && unzip {join(dist_path, packing_name)} && rm {join(dist_path, packing_name)}'
                     .replace('\\', '/'))
    stdin, stdout, stderr = ssh_client.exec_command(unzip_command)
    output = stdout.read()
    error = stderr.read()
    print("输出：", output.decode())
    if error:
        print("错误：", error.decode())

    sftp_client.close()
    ssh_client.close()
    remove(join(dirname(packing_path), packing_name))
