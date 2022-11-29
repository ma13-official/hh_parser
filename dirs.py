import os


class Dirs:
    @staticmethod
    def make_dir(path, directory):
        os.chdir(path)
        if not os.path.exists(os.path.join(path, directory)):
            os.mkdir(directory)

    @staticmethod
    def check_file(path, file):
        return os.path.exists(os.path.join(path, file))
