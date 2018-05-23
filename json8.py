#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with JSON
"""
__version__ = "0.0.6"


class Json:
    """Class to work with JSON
    """
    @classmethod
    def check(cls, filename):
        """
        :param filename: string with path to JSON file
        :return: boolean with state of JSON correctness
        """
        try:
            cls.load(filename)
            return True
        except:  # pylint: disable=bare-except
            print("JSON is bad")
            return False

    @classmethod
    def save(cls, filename, json_string, quiet=False, debug=False):
        """
        :param filename: path of file, where JSON will be saved
        :param json_string: list or dict to save in file
        :param quiet: suppress print to console
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
        json_test_string = cls.load(filename, quiet=True)
        if json_string != json_test_string:
            from .path8 import Path
            from .print8 import Print
            Print.debug("jsonstring_to_save", json_string, "json_test_string_from_file", json_test_string)
            raise IOError("error while saving JSON, try to repair script at path " +
                          Path.full(sys.argv[0]))  # exception

    @classmethod
    def load(cls, filename, quiet=False, debug=False):
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
