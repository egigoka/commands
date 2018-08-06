#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with JSON
"""
__version__ = "2.3.0"


class Json:
    """Class to work with JSON
    """

    @classmethod
    def __init__(cls, filename, quiet=True):
        cls.filename = filename
        if cls._check_file(filename):
            cls.string = cls._load_from_file(cls.filename, quiet=quiet)
        else:
            cls.string = {}
            cls._save_to_file(cls.filename, cls.string, quiet=quiet)

    @classmethod
    def load(cls, quiet=True):
        """Loads json from file, defined in class init to class var "string"
        :param quiet: boolean, suppress print to console
        :return: None
        """
        cls.string = cls._load_from_file(cls.filename, quiet=quiet)

    @classmethod
    def save(cls, quiet=True, debug=False):
        """Saves json to file, defined in class init from class var "string"
        :param quiet: boolean, suppress print to console
        :param debug: boolean, prints some more info
        :return: None
        """
        cls._save_to_file(cls.filename, cls.string, quiet=quiet, debug=debug)

    @classmethod
    def _check_file(cls, filename, quiet=True):
        """
        :param filename: string with path to JSON file
        :return: boolean with state of JSON correctness
        """
        try:
            cls._load_from_file(filename, quiet=quiet)
            return True
        except:  # pylint: disable=bare-except
            if not quiet:
                print("JSON is bad")
            return False

    @classmethod
    def _save_to_file(cls, filename, json_string, quiet=False, debug=False):
        """
        :param filename: path of file, where JSON will be saved
        :param json_string: list or dict to save in file
        :param quiet: boolean, suppress print to console
        :param debug: boolean, needed for debugging
        :return:
        """
        import json
        import sys
        from .file8 import File
        try:
            File.wipe(filename)
            settings_json_text_io = open(filename, "w")
            json.dump(json_string, settings_json_text_io)
            settings_json_text_io.close()
            if not quiet:
                print("JSON succesfull saved")
            if debug:
                print("sys.argv[0] =", sys.argv[0])
                print(json_string)
        except:
            from .path8 import Path
            raise IOError("error while saving JSON, try to repair script at path " +
                          Path.full(sys.argv[0]))
        json_test_string = cls._load_from_file(filename, quiet=True)
        if json_string != json_test_string:
            from .path8 import Path
            from .print8 import Print
            Print.debug("jsonstring_to_save", json_string, "json_test_string_from_file", json_test_string)
            raise IOError("error while saving JSON, try to repair script at path " +
                          Path.full(sys.argv[0]))

    @classmethod
    def _load_from_file(cls, filename, quiet=False, debug=False):
        """
        :param filename: path of file, from load JSON
        :param quiet: suppress print to console
        :param debug: boolean, needed for debugging
        :return:
        """
        import json
        import os
        try:
            if not os.path.isfile(filename):
                from .file8 import File
                File.create(filename)
                cleanjson = {}
                cls.save(filename, cleanjson)
            settings_json_text_io = open(filename)
            json_string_in_memory = json.load(settings_json_text_io)
            settings_json_text_io.close()
            if not quiet:
                print("JSON succesfull loaded")
            if debug:
                print(json_string_in_memory)
            return json_string_in_memory
        except:
            import sys
            from .path8 import Path
            raise IOError("error while loading JSON, try to repair script at path " +
                          Path.full(sys.argv[0]))
