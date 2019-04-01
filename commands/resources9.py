#! python3
# -*- coding: utf-8 -*-

__version__ = "0.1.0"

class Resources:
    @classmethod
    def to_file(cls, name, path):
        from.base64_9 import Base64
        from .os9 import OS
        string = cls.resources_dict[f"{name.lower()}_{OS.name}_{OS.architecture}"]
        return Base64.to_file(string, path)

    resources_dict = {
        #"wget_windows_x32": "",
        #"wget_windows_x64": ""
        "psexec_windows_64bit": "",
        "psexec_windows_32bit": "",
    }