import os


# DIRECTORY FUNCTIONS
def dir_create(path):
    """Checks if path exists, if not, creates it."""
    if not os.path.isdir(path):
        os.mkdir(path)


def dir_remove(path):
    os.rmdir(path)


def dir_exists(dirpath):
    return os.path.isdir(dirpath)


# FILE FUNCTIONS
def file_exists(filepath):
    return os.path.isfile(filepath)


def file_delete(filepath):
    if file_exists(filepath):
        os.remove(filepath)


def file_create(filepath):
    if not file_exists(filepath):
        f = open(filepath, 'x')
    # try:
    #     f = open(filepath, "x")
    # except Exception as e:
    #     print(e.args)


class StandardAppDirStruct:
    def __init__(self, app_dir, app_name):
        self.app_dir = app_dir
        self.app_name = app_name

        # DATA DIRECTORY
        self.data_dir = '{}\\data_{}'.format(self.app_dir, self.app_name)
        dir_create(self.data_dir)
        # LOGS DIRECTORY
        self.logs_dir = '{}\\logs'.format(self.data_dir)
        dir_create(self.logs_dir)
        # RESOURCES DIRECTORY
        self.resources_dir = '{}\\resources'.format(self.data_dir)
        dir_create(self.resources_dir)

# if __name__ == '__main__':
#     return
