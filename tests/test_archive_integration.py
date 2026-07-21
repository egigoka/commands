# Consolidated tests for commands/archive.py (integration)

import os
import shutil
import tempfile
import zipfile

from commands.archive import Archive


import tarfile
import pytest

def test_Archive_zip():
    temp_dir = tempfile.mkdtemp()
    try:
        file_path = os.path.join(temp_dir, 'test.txt')
        file_content = 'Hello, world!'
        with open(file_path, 'w') as f:
            f.write(file_content)

        zip_path = os.path.join(temp_dir, 'archive.zip')
        Archive(zip_path, archive_type=Archive.MODE_ZIPDEFLATED, mode='w').file(
            file_path,
            arcname='test.txt'
        )

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
        Archive(zip_path, archive_type=Archive.MODE_ZIPDEFLATED, mode='w').file(
            file_path,
            arcname='test.txt'
        )

        assert os.path.exists(zip_path)

        # Now let's check the contents of the archive
        with zipfile.ZipFile(zip_path, 'r') as myzip:
            with myzip.open('test.txt') as myfile:
                assert myfile.read().decode() == file_content
    finally:
        shutil.rmtree(temp_dir)

def test_Archive_extract_single():
    temp_dir = tempfile.mkdtemp()
    try:
        file_path = os.path.join(temp_dir, 'test.txt')
        file_content = 'Hello, world!'
        with open(file_path, 'w') as f:
            f.write(file_content)

        zip_path = os.path.join(temp_dir, 'archive.zip')
        Archive(zip_path, archive_type=Archive.MODE_ZIPDEFLATED, mode='w').file(
            file_path,
            arcname='test.txt'
        )

        extracted_path = os.path.join(temp_dir, 'extracted.txt')
        Archive(zip_path, archive_type=Archive.MODE_ZIPDEFLATED).extract('test.txt', extracted_path)

        assert os.path.exists(extracted_path)
        with open(extracted_path, 'r') as f:
            assert f.read() == file_content
    finally:
        shutil.rmtree(temp_dir)

def test_Archive_tar_lzma():
    """Test Archive with tar.lzma (tar.xz) format"""
    temp_dir = tempfile.mkdtemp()
    try:
        file_path = os.path.join(temp_dir, 'test.txt')
        file_content = 'Hello, tar.lzma!'
        with open(file_path, 'w') as f:
            f.write(file_content)

        tar_path = os.path.join(temp_dir, 'archive.tar.xz')
        Archive(tar_path, archive_type=Archive.MODE_TARLZMA, mode='w').file(
            file_path,
            arcname='test.txt'
        )

        assert os.path.exists(tar_path)

        # Verify contents
        with tarfile.open(tar_path, 'r:xz') as tar:
            members = tar.getnames()
            assert 'test.txt' in members
            extracted = tar.extractfile('test.txt')
            assert extracted.read().decode() == file_content
    finally:
        shutil.rmtree(temp_dir)

def test_Archive_tar_gz():
    """Test Archive with tar.gz format"""
    temp_dir = tempfile.mkdtemp()
    try:
        file_path = os.path.join(temp_dir, 'test.txt')
        file_content = 'Hello, tar.gz!'
        with open(file_path, 'w') as f:
            f.write(file_content)

        tar_path = os.path.join(temp_dir, 'archive.tar.gz')
        Archive(tar_path, archive_type=Archive.MODE_TARGZ, mode='w').file(
            file_path,
            arcname='test.txt'
        )

        assert os.path.exists(tar_path)

        # Verify contents
        with tarfile.open(tar_path, 'r:gz') as tar:
            members = tar.getnames()
            assert 'test.txt' in members
            extracted = tar.extractfile('test.txt')
            assert extracted.read().decode() == file_content
    finally:
        shutil.rmtree(temp_dir)

def test_Archive_dir():
    """Test archiving an entire directory"""
    temp_dir = tempfile.mkdtemp()
    try:
        # Create a test directory structure
        input_dir = os.path.join(temp_dir, 'test_dir')
        os.makedirs(input_dir)
        os.makedirs(os.path.join(input_dir, 'subdir'))

        # Create test files
        with open(os.path.join(input_dir, 'file1.txt'), 'w') as f:
            f.write('Content 1')
        with open(os.path.join(input_dir, 'file2.txt'), 'w') as f:
            f.write('Content 2')
        with open(os.path.join(input_dir, 'subdir', 'file3.txt'), 'w') as f:
            f.write('Content 3')

        zip_path = os.path.join(temp_dir, 'archive.zip')
        Archive(zip_path, archive_type=Archive.MODE_ZIPDEFLATED).dir(
            input_dir,
            verbose=False
        )

        assert os.path.exists(zip_path)

        # Verify all files are in the archive
        with zipfile.ZipFile(zip_path, 'r') as myzip:
            names = myzip.namelist()
            assert 'file1.txt' in names
            assert 'file2.txt' in names
            assert 'subdir/file3.txt' in names or 'subdir\\file3.txt' in names  # OS-dependent path separator

            # Verify content of one file
            with myzip.open('file1.txt') as myfile:
                assert myfile.read().decode() == 'Content 1'
    finally:
        shutil.rmtree(temp_dir)

def test_Archive_dir_tar_gz():
    """Test archiving directory to tar.gz format"""
    temp_dir = tempfile.mkdtemp()
    try:
        input_dir = os.path.join(temp_dir, 'test_dir')
        os.makedirs(input_dir)

        with open(os.path.join(input_dir, 'file1.txt'), 'w') as f:
            f.write('Content 1')
        with open(os.path.join(input_dir, 'file2.txt'), 'w') as f:
            f.write('Content 2')

        tar_path = os.path.join(temp_dir, 'archive.tar.gz')
        Archive(tar_path, archive_type=Archive.MODE_TARGZ).dir(
            input_dir,
            verbose=False
        )

        assert os.path.exists(tar_path)

        # Verify contents
        with tarfile.open(tar_path, 'r:gz') as tar:
            names = tar.getnames()
            assert 'file1.txt' in names
            assert 'file2.txt' in names
    finally:
        shutil.rmtree(temp_dir)

def test_Archive_extract_all():
    """Test extracting all files from an archive"""
    temp_dir = tempfile.mkdtemp()
    try:
        # Create and archive some files
        input_dir = os.path.join(temp_dir, 'input')
        os.makedirs(input_dir)

        with open(os.path.join(input_dir, 'file1.txt'), 'w') as f:
            f.write('Content 1')
        with open(os.path.join(input_dir, 'file2.txt'), 'w') as f:
            f.write('Content 2')

        zip_path = os.path.join(temp_dir, 'archive.zip')
        Archive(zip_path, archive_type=Archive.MODE_ZIPDEFLATED).dir(
            input_dir,
            verbose=False
        )

        # Extract all files
        output_dir = os.path.join(temp_dir, 'output')
        os.makedirs(output_dir)
        Archive(zip_path, archive_type=Archive.MODE_ZIPDEFLATED).extract_all(output_dir)

        # Verify extracted files
        assert os.path.exists(os.path.join(output_dir, 'file1.txt'))
        assert os.path.exists(os.path.join(output_dir, 'file2.txt'))

        with open(os.path.join(output_dir, 'file1.txt'), 'r') as f:
            assert f.read() == 'Content 1'
    finally:
        shutil.rmtree(temp_dir)

def test_Archive_extract_all_tar_lzma():
    """Test extracting all files from tar.lzma archive"""
    temp_dir = tempfile.mkdtemp()
    try:
        input_dir = os.path.join(temp_dir, 'input')
        os.makedirs(input_dir)

        with open(os.path.join(input_dir, 'file1.txt'), 'w') as f:
            f.write('Content 1')

        tar_path = os.path.join(temp_dir, 'archive.tar.xz')
        Archive(tar_path, archive_type=Archive.MODE_TARLZMA).dir(
            input_dir,
            verbose=False
        )

        output_dir = os.path.join(temp_dir, 'output')
        os.makedirs(output_dir)
        Archive(tar_path, archive_type=Archive.MODE_TARLZMA).extract_all(output_dir)

        assert os.path.exists(os.path.join(output_dir, 'file1.txt'))
        with open(os.path.join(output_dir, 'file1.txt'), 'r') as f:
            assert f.read() == 'Content 1'
    finally:
        shutil.rmtree(temp_dir)

def test_Archive_file_with_arcname():
    """Test archiving with custom arcname"""
    temp_dir = tempfile.mkdtemp()
    try:
        file_path = os.path.join(temp_dir, 'original.txt')
        with open(file_path, 'w') as f:
            f.write('Test content')

        zip_path = os.path.join(temp_dir, 'archive.zip')
        Archive(zip_path, mode='w').file(file_path, arcname='custom_name.txt')

        with zipfile.ZipFile(zip_path, 'r') as myzip:
            assert 'custom_name.txt' in myzip.namelist()
            with myzip.open('custom_name.txt') as myfile:
                assert myfile.read().decode() == 'Test content'
    finally:
        shutil.rmtree(temp_dir)

def test_Archive_extract_single_tar_gz():
    """Test extracting single file from tar.gz archive"""
    temp_dir = tempfile.mkdtemp()
    try:
        file_path = os.path.join(temp_dir, 'test.txt')
        with open(file_path, 'w') as f:
            f.write('Test content')

        tar_path = os.path.join(temp_dir, 'archive.tar.gz')
        Archive(tar_path, archive_type=Archive.MODE_TARGZ, mode='w').file(
            file_path,
            arcname='test.txt'
        )

        extracted_path = os.path.join(temp_dir, 'extracted.txt')
        Archive(tar_path, archive_type=Archive.MODE_TARGZ).extract(
            'test.txt',
            extracted_path
        )

        assert os.path.exists(extracted_path)
        with open(extracted_path, 'r') as f:
            assert f.read() == 'Test content'
    finally:
        shutil.rmtree(temp_dir)

def test_Archive_file_append_mode_nonexistent_archive():
    """Test Archive.file with append mode when archive doesn't exist"""
    temp_dir = tempfile.mkdtemp()
    try:
        file_path = os.path.join(temp_dir, 'test.txt')
        with open(file_path, 'w') as f:
            f.write('Test content')

        zip_path = os.path.join(temp_dir, 'archive.zip')
        # Use append mode on non-existent archive - should create it via temp file
        Archive(zip_path, archive_type=Archive.MODE_ZIPDEFLATED, mode='a').file(
            file_path,
            arcname='test.txt'
        )

        assert os.path.exists(zip_path)

        # Verify the file was archived
        with zipfile.ZipFile(zip_path, 'r') as myzip:
            assert 'test.txt' in myzip.namelist()
            with myzip.open('test.txt') as myfile:
                assert myfile.read().decode() == 'Test content'
    finally:
        shutil.rmtree(temp_dir)

def test_Archive_dir_verbose(capsys):
    """Test Archive.dir with verbose=True to trigger print output"""
    temp_dir = tempfile.mkdtemp()
    try:
        input_dir = os.path.join(temp_dir, 'test_dir')
        os.makedirs(input_dir)

        # Create test file
        with open(os.path.join(input_dir, 'file1.txt'), 'w') as f:
            f.write('Content 1')

        zip_path = os.path.join(temp_dir, 'archive.zip')
        # Use verbose=True to trigger the print statements
        Archive(zip_path, archive_type=Archive.MODE_ZIPDEFLATED).dir(
            input_dir,
            verbose=True
        )

        assert os.path.exists(zip_path)

        # Check that output was printed
        captured = capsys.readouterr()
        assert "archived" in captured.out or "file1.txt" in captured.out
    finally:
        shutil.rmtree(temp_dir)

def test_archive_instance_add_file():
    temp_dir = tempfile.mkdtemp()
    try:
        file_path = os.path.join(temp_dir, 'test.txt')
        with open(file_path, 'w') as f:
            f.write('data')

        archive_path = os.path.join(temp_dir, 'archive.zip')
        arch = Archive(archive_path, mode='w')
        arch.add_file(file_path, arcname='test.txt')

        assert os.path.exists(archive_path)
    finally:
        shutil.rmtree(temp_dir)

def test_unarchive_instance_extract_all():
    temp_dir = tempfile.mkdtemp()
    try:
        # Prepare archive
        file_path = os.path.join(temp_dir, 'test.txt')
        with open(file_path, 'w') as f:
            f.write('data')
        archive_path = os.path.join(temp_dir, 'archive.zip')
        Archive(archive_path, mode='w').file(file_path, arcname='test.txt')

        # Extract using instance
        output_dir = os.path.join(temp_dir, 'out')
        arch = Archive(archive_path)
        arch.extract_all(output_dir)

        assert os.path.exists(os.path.join(output_dir, 'test.txt'))
    finally:
        shutil.rmtree(temp_dir)

class TestArchiveCoverage:
    """Tests to improve Archive module coverage"""
    def test_archive_add_dir(self):
        """Test Archive.add_dir instance method (lines 79-80)"""
        temp_dir = tempfile.mkdtemp()
        try:
            input_dir = os.path.join(temp_dir, "input_dir")
            os.makedirs(input_dir)
            with open(os.path.join(input_dir, "file1.txt"), "w") as f:
                f.write("data")

            archive_path = os.path.join(temp_dir, "test.zip")
            c = Archive(archive_file=archive_path, archive_type=Archive.MODE_ZIPDEFLATED)
            c.add_dir(input_dir=input_dir, verbose=False)

            with zipfile.ZipFile(archive_path, "r") as zf:
                assert "file1.txt" in zf.namelist()
        finally:
            shutil.rmtree(temp_dir)
    def test_archive_extract_single_file(self):
        """Test Archive.extract instance method for a single file."""
        temp_dir = tempfile.mkdtemp()
        try:
            file_path = os.path.join(temp_dir, "test.txt")
            with open(file_path, "w") as f:
                f.write("content")

            archive_path = os.path.join(temp_dir, "test.zip")
            Archive(archive_file=archive_path, mode="w").file(file_path, arcname="test.txt")

            output_path = os.path.join(temp_dir, "output.txt")
            Archive(archive_file=archive_path).extract("test.txt", output_path)

            assert os.path.exists(output_path)
        finally:
            shutil.rmtree(temp_dir)
