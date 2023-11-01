import os
import csv

USER_PROPERTIES = ['id', 'name', 'permission', 'date']


class InvalidStorageStructureException(Exception):
    def __init__(self, message: str = ''):
        self.message = 'Invalid storage structure. \n' + message
        super().__init__(self.message)


class Storage:
    def __init__(self, storage_path):
        self.__storage_path = storage_path
        self.__validate()

    def __validate(self, forced: bool = True):
        self.__subjects_folder = os.path.join(self.__storage_path, 'subjects')
        self.__students_file = os.path.join(self.__storage_path, 'students.csv')

        if not os.path.exists(self.__subjects_folder) or not os.path.isdir(self.__subjects_folder):
            if forced:
                os.makedirs(self.__subjects_folder)
            else:
                raise InvalidStorageStructureException('Invalid storage structure. Subjects folder is missing.')

        if not os.path.exists(self.__students_file) or not os.path.isfile(self.__students_file):
            if forced:
                with open(self.__students_file, 'w', newline=''):
                    pass
            else:
                raise InvalidStorageStructureException('Invalid storage structure. Students file missing.')

    def get_users(self, permission: int = 0):
        result = list()
        with open(self.__students_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=USER_PROPERTIES)
            for row in reader:
                if int(row['permission']) >= permission:
                    result.append(row)
        return result

    def create_user(self, user_id, user_name):
        with open(self.__students_file, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=USER_PROPERTIES)
            writer.writerow({'id': user_id, 'name': user_name, 'permission': 0, 'date': None})

    def get_user(self, user_id):
        with open(self.__students_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=USER_PROPERTIES)
            for row in reader:
                if row['id'] == str(user_id):
                    return row
        return False
