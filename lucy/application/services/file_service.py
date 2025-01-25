import base64
import binascii
import os
import uuid

from lucy.domain.models.file import File


class FileService:
    def __init__(self, upload_dir: str):
        self.upload_dir = upload_dir
        os.makedirs(self.upload_dir, exist_ok=True)

    def upload_file(self, file_name: str, file_content_base64: str) -> str:
        file_extension = os.path.splitext(file_name)[1]
        new_file_name = f"{uuid.uuid4()}{file_extension}"
        try:
            file_content = base64.b64decode(file_content_base64)
        except (ValueError, binascii.Error) as e:
            raise ValueError(f"Error decoding base64 content for file {file_name}: {e}")
        file = File(new_file_name, file_content)
        file_path = os.path.join(self.upload_dir, new_file_name)
        file.save_to_path(file_path)
        relative_path = os.path.relpath(file_path, start='static').replace('\\', '/')
        print(f"path de la imagen /static/{relative_path}")
        return f'/static/{relative_path}'
