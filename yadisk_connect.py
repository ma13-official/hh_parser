import yadisk
import os
import posixpath
from time import perf_counter as pc


class YaDisk:
    @staticmethod
    def write_on_yadisk():
        y = YaDisk.connect()

        directory = "vacancies_per_day"

        for filename in os.scandir(directory):
            print(filename.name)
            f = open(filename, 'rb')
            if not y.is_file("/Dashboard_Vacancies/Datasets/" + filename.name):
                y.upload(f, "/Dashboard_Vacancies/Datasets/" + filename.name)

    @staticmethod
    def connect():
        TOKEN = "y0_AgAAAABk-5pfAADLWwAAAADTaONM6iu7zLEeRJ-KX6WNvrzeaO73tgo"
        y = yadisk.YaDisk(token=TOKEN)

        return y

    @staticmethod
    def download(path, directory):

        y = YaDisk.connect()

        for file in y.get_files():
            file['path'] = file['path'][5:]
            if file['path'].startswith(path):
                YaDisk.add_file_with_path(directory, file, y)

    @staticmethod
    def add_file_with_path(directory, file, y):
        os.chdir(directory)
        folder_name = ""
        if_folder_name = False
        path = file['path']
        for symbol in path:
            if if_folder_name:
                if symbol == "/":
                    if not os.path.isdir(folder_name):
                        os.mkdir(folder_name)
                    os.chdir(folder_name)
                    folder_name = ""
                else:
                    folder_name += symbol
            if symbol == "/":
                if_folder_name = True
        y.download(file['path'], directory + file['path'])

    @staticmethod
    def upload(from_dir, to_dir):
        y = YaDisk.connect()

        for root, dirs, files in os.walk(from_dir):
            p = root.split(from_dir)[1].strip(os.path.sep).replace(os.path.sep, "/")
            dir_path = posixpath.join(to_dir, p)

            try:
                y.mkdir(dir_path)
            except yadisk.exceptions.PathExistsError:
                pass

            for file in files:
                file_path = posixpath.join(dir_path, file)
                print(file_path)
                p_sys = p.replace("/", os.path.sep)
                in_path = os.path.join(from_dir, p_sys, file)
                try:
                    y.upload(in_path, file_path)
                except yadisk.exceptions.PathExistsError:
                    pass


# start = pc()
# YaDisk.upload("C:/Users/mi/OneDrive - ITMO UNIVERSITY/education", "education")
# print(pc() - start)
# YaDisk.download("/test", "C:/Users/mi/OneDrive - ITMO UNIVERSITY/work/hh_parser/123")

