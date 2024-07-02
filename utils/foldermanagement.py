import os

class Foldermanagement:
    def _create_directory(self, path):
        if not os.path.exists(path):
            print(f"The path {path} does not exist. Creating.")
            os.makedirs(path)
        return path