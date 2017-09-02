import os


class DBFileKeeper:
    def __init__(self, db_file_name):
        self.db_folder = "DataBase"
        self.db_file_name = db_file_name
        self.full_db_file_path = os.path.join(self.db_folder, self.db_file_name)

    def is_exist(self):
        return os.path.exists(self.full_db_file_path)

    def create_db_file(self):
        try:
            with open(self.full_db_file_path, "w"):
                pass
        except OSError as err:
            print(err)
            return False
        return True

    def delete_db_file(self):
        try:
            os.remove(self.full_db_file_path)
        except OSError as err:
            print(err)
            return False
        return True

    def get_path(self):
        return self.full_db_file_path
