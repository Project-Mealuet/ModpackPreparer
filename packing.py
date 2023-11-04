from configparser import ConfigParser
from json import load
from os import walk
from os.path import join, relpath, dirname, basename
from zipfile import ZipFile, ZIP_DEFLATED


def zipdir(directory_to_zip, zip_filename):
    with ZipFile(zip_filename, 'w', ZIP_DEFLATED) as zipf:
        for root, _, files in walk(directory_to_zip):
            for file in files:
                full_path = join(root, file)
                # 使用ZIP文件的名称（不带后缀）作为前缀创建存储路径
                archive_path = join(basename(zip_filename).rsplit('.', 1)[0], relpath(full_path, directory_to_zip))
                zipf.write(full_path, archive_path)


config = ConfigParser()
config.read('config.ini', encoding='UTF-8')
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
zipdir(packing_path, join(dirname(packing_path), packing_name))
