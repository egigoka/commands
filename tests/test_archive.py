# Consolidated tests for commands/archive.py (unit)

# ---- from test_archive9.py ----




import os
import tempfile
import shutil
import zipfile
import tarfile
import pytest
from commands.archive import Archive































if __name__ == '__main__':
    pytest.main([__file__, '-v'])




# ---- from test_archive9_instance.py ----




import tempfile
import shutil
import os
from commands.archive import Archive








# ---- from test_archive_coverage.py ----




import os
import tempfile
import shutil
import zipfile
import pytest
from commands.archive import Archive


class TestArchiveCoverage:
    """Tests to improve Archive module coverage"""


    def test_archive_path_property(self):
        """Test Archive.path property (line 68)"""
        c = Archive(archive_file="test.zip")
        assert c.path == "test.zip"



    def test_archive_write_fallback(self):
        """Exercise Archive._write fallback branch."""
        class DummyArchive:
            def __init__(self):
                self.called = False
                self.args = None
                self.kwargs = None

            def write(self, *args, **kwargs):
                self.called = True
                self.args = args
                self.kwargs = kwargs
                return "ok"

        dummy = DummyArchive()
        archive = Archive(archive_file="test.zip")
        result = archive._write(dummy, "in.txt", arcname="in.txt", archive_type=999)

        assert result == "ok"
        assert dummy.called
        assert dummy.args[0] == "in.txt"
        assert dummy.kwargs["arcname"] == "in.txt"
