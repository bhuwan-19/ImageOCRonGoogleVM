import os

from settings import ROOT_DIR


def load_text(filename):

    if os.path.isfile(filename):
        file = open(filename, 'r')
        text = file.read()
        file.close()
    else:
        text = ''

    return text


def save_file(content, filename, method):

    file = open(filename, method)
    file.write(content)
    file.close()

    return


def create_folder_by_filepath(filepath):

    root_directory = os.path.join(ROOT_DIR, 'output')

    no_head_path = filepath[6:]
    no_head_tail_path = no_head_path[:-4]
    folder_list = no_head_tail_path.split("/")

    for folder in folder_list[:-1]:

        root_directory = os.path.join(root_directory, folder)
        if os.path.isdir(root_directory):
            continue
        else:
            os.mkdir(root_directory)

    return no_head_tail_path
