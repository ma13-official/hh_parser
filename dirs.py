import os


class Dirs:
    @staticmethod
    def make_dir(path, directory):
        os.chdir(path)
        if not os.path.exists(os.path.join(path, directory)):
            os.mkdir(directory)
