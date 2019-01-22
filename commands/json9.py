#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with JSON
"""
__version__ = "2.4.1"


class Json:
    """Class to work with JSON
    """

    def __init__(self, filename, quiet=True, ensure_ascii=False):
        self.filename = filename
        self.ensure_ascii = ensure_ascii
        if self._check_file(filename):
            self.string = self._load_from_file(self.filename, quiet=quiet)
        else:
            self.string = {}
            self._save_to_file(self.filename, self.string, quiet=quiet)

    def load(self, quiet=True):
        """Loads json from file, defined in class init to class var "string"
        :param quiet: boolean, suppress print to console
        :return: None
        """
        self.string = self._load_from_file(self.filename, quiet=quiet)

    def save(self, quiet=True, debug=False):
        """Saves json to file, defined in class init from class var "string"
        :param quiet: boolean, suppress print to console
        :param debug: boolean, prints some more info
        :return: None
        """
        if debug:
            print(self.string)
        self._save_to_file(self.filename, self.string, quiet=quiet, debug=debug)

    def _check_file(self, filename, quiet=True):
        """
        :param filename: string with path to JSON file
        :return: boolean with state of JSON correctness
        """
        # try:
        self._load_from_file(filename, quiet=quiet)
        return True
        # except:  # pylint: disable=bare-except
        #     if not quiet:
        #         print("JSON is bad")
        #     return False

    def _save_to_file(self, filename, json_string, quiet=False, debug=False):
        """
        :param filename: path of file, where JSON will be saved
        :param json_string: list or dict to save in file
        :param quiet: boolean, suppress print to console
        :param debug: boolean, needed for debugging
        :return:
        """
        import json
        import sys
        from .file9 import File
        if debug:
            print("sys.argv[0] =", sys.argv[0])
            print(json_string)
        # try:
        File.wipe(filename)
        settings_json_text_io = open(filename, "w")
        json.dump(json_string, settings_json_text_io, ensure_ascii=self.ensure_ascii)
        settings_json_text_io.close()
        if not quiet:
            print("JSON succesfull saved")
        # except:
        #     from .path import Path
        #     raise IOError("error while saving JSON, try to repair script at path " +
        #                   Path.full(sys.argv[0]))
        json_test_string = self._load_from_file(filename, quiet=True)
        if json_string != json_test_string:
            from .path9 import Path
            from .print9 import Print
            Print.debug("jsonstring_to_save", json_string, "json_test_string_from_file", json_test_string)
            raise IOError("error while saving JSON, try to repair script at path " +
                          Path.full(sys.argv[0]))

    def _load_from_file(self, filename, quiet=False, debug=False):
        """
        :param filename: path of file, from load JSON
        :param quiet: suppress print to console
        :param debug: boolean, needed for debugging
        :return:
        """
        import json
        import os
        # try:
        if not os.path.isfile(filename):
            from .file9 import File
            File.create(filename)
            clean_json = {}
            self._save_to_file(filename, clean_json)
        settings_json_text_io = open(filename)
        json_string_in_memory = json.load(settings_json_text_io)
        settings_json_text_io.close()
        if not quiet:
            print("JSON succesfull loaded")
        if debug:
            print(json_string_in_memory)
        return json_string_in_memory
        # except:
        #     import sys
        #     from .path import Path
        #     raise IOError("error while loading JSON, try to repair script at path " +
        #                   Path.full(sys.argv[0]))