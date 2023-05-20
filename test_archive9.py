import os
import tempfile
import shutil
import zipfile
from commands.archive9 import UniversalArchive, Archive, Unarchive  # Replace 'your_module' with the actual name of your module

def test_UniversalArchive_zip():
    temp_dir = tempfile.mkdtemp()
    try:
        file_path = os.path.join(temp_dir, 'test.txt')
        file_content = 'Hello, world!'
        with open(file_path, 'w') as f:
            f.write(file_content)

        zip_path = os.path.join(temp_dir, 'archive.zip')
        archive = UniversalArchive(zip_path, 'w', Archive.MODE_ZIPDEFLATED)
        archive.write(file_path, 'test.txt')
        archive.close()

        assert os.path.exists(zip_path)

        # Now let's check the contents of the archive
        with zipfile.ZipFile(zip_path, 'r') as myzip:
            with myzip.open('test.txt') as myfile:
                assert myfile.read().decode() == file_content
    finally:
        shutil.rmtree(temp_dir)


def test_Archive_file():
    temp_dir = tempfile.mkdtemp()
    try:
        file_path = os.path.join(temp_dir, 'test.txt')
        file_content = 'Hello, world!'
        with open(file_path, 'w') as f:
            f.write(file_content)

        zip_path = os.path.join(temp_dir, 'archive.zip')
        Archive.file(file_path, zip_path, arcname='test.txt', mode='w', archive_type=Archive.MODE_ZIPDEFLATED)

        assert os.path.exists(zip_path)

        # Now let's check the contents of the archive
        with zipfile.ZipFile(zip_path, 'r') as myzip:
            with myzip.open('test.txt') as myfile:
                assert myfile.read().decode() == file_content
    finally:
        shutil.rmtree(temp_dir)


def test_Unarchive_single():
    temp_dir = tempfile.mkdtemp()
    try:
        file_path = os.path.join(temp_dir, 'test.txt')
        file_content = 'Hello, world!'
        with open(file_path, 'w') as f:
            f.write(file_content)

        zip_path = os.path.join(temp_dir, 'archive.zip')
        Archive.file(file_path, zip_path, arcname='test.txt', mode='w', archive_type=Archive.MODE_ZIPDEFLATED)

        extracted_path = os.path.join(temp_dir, 'extracted.txt')
        Unarchive.single(zip_path, 'test.txt', extracted_path, archive_type=Archive.MODE_ZIPDEFLATED)

        assert os.path.exists(extracted_path)
        with open(extracted_path, 'r') as f:
            assert f.read() == file_content
    finally:
        shutil.rmtree(temp_dir)
