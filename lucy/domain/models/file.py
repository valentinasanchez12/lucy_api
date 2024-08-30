class File:
    def __init__(self, file_name: str, file_content: bytes):
        self.file_name = file_name
        self.file_content = file_content
        self.file_path = None

    def save_to_path(self, path: str):
        self.file_path = path
        with open(self.file_path, 'wb') as file_object:
            file_object.write(self.file_content)
