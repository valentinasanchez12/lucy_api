import base64
import os

from lucy.domain.models.file import File


class FileService:
    def __init__(self, upload_dir: str):
        self.upload_dir = upload_dir
        os.makedirs(self.upload_dir, exist_ok=True)

    def upload_file(self, file_name: str, file_content_base64: str) -> str:
        file_content = base64.b64decode(file_content_base64)
        file = File(file_name, file_content)
        file_path = os.path.join(self.upload_dir, file_name)
        file.save_to_path(file_path)
        relative_path = os.path.relpath(file_path, start='static').replace('\\', '/')
        return relative_path
