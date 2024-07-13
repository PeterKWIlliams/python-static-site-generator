import os
import shutil


def copy_files(source, destination_base="public"):
    paths = os.listdir(source)
    for path in paths:
        source_path = os.path.join(source, path)
        destination_path = os.path.join(destination_base, path)
        if os.path.isdir(source_path):
            os.mkdir(destination_path)
            copy_files(source_path, destination_path)
        if os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)


def generate_files(source, destination_base="public"):
    if os.path.exists(destination_base):
        shutil.rmtree(destination_base)
    os.mkdir(destination_base)
    copy_files(source)
