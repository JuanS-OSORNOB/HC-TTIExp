import os

class Foldermanagement:
    def _create_directory(self, path):
        if not os.path.join(path):
            os.makedirs(path)