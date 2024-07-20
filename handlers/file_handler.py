import os
import zipfile
import tempfile
from contextlib import contextmanager

class FileHandler:
    @contextmanager
    def create_temp_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir

    def create_zip_file(self, directory):
        zip_path = os.path.join(tempfile.gettempdir(), 'youtube_audio.zip')
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, directory)
                    zipf.write(file_path, arcname)
        return zip_path

    def remove_file(self, file_path):
        os.remove(file_path)