import os


class InvalidStorageStructureException(Exception):
    def __init__(self, message: str = ''):
        self.message = 'Invalid storage structure. \n' + message
        super().__init__(self.message)


class Storage:
    def __init__(self, storage_path):
        self.storage_path = storage_path

    def validate(self, forced: bool = True):

        subjects_folder = os.path.join(self.storage_path, 'subjects')
        if not os.path.exists(subjects_folder) or not os.path.isdir(subjects_folder):
            if forced:
                os.makedirs(subjects_folder)
            else:
                raise InvalidStorageStructureException('Invalid storage structure. Subjects folder is missing.')
        students_file = os.path.join(self.storage_path, 'students.csv')
        if not os.path.exists(students_file) or not os.path.isfile(students_file):
            if forced:
                with open(students_file, 'w', newline=''):
                    pass
            else:
                raise InvalidStorageStructureException('Invalid storage structure. Students file missing.')
