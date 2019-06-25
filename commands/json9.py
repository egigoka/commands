#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with JSON
"""
__version__ = "2.6.2"


class Json:
    """Class to work with JSON
    """

    def __init__(self, filename, quiet=True, ensure_ascii=False, debug=False):
        self.filename = filename
        self.ensure_ascii = ensure_ascii
        self.quiet = quiet
        self.debug = debug
        if self._check_file(filename):
            self.string = self._load_from_file(self.filename, quiet=quiet)
        else:
            self.string = {}
            self._save_to_file(self.filename, self.string, quiet=quiet)

    def __getitem__(self, item):
        self.save(quiet=self.quiet, debug=self.debug)
        return self.string.__getitem__(item)

    def __setitem__(self, key, value):
        self.save(quiet=self.quiet, debug=self.debug)
        return self.string.__setitem__(key, value)

    def load(self, quiet=True):
        """Loads json from file, defined in class init to class var "string"
        <br>`param quiet` boolean, suppress print to console
        <br>`return` None
        """
        self.string = self._load_from_file(self.filename, quiet=quiet)

    def save(self, quiet=True, debug=False):
        """Saves json to file, defined in class init from class var "string"
        <br>`param quiet` boolean, suppress print to console
        <br>`param debug` boolean, prints some more info
        <br>`return` None
        """
        if debug:
            print(self.string)
        self._save_to_file(self.filename, self.string, quiet=quiet, debug=debug)

    def _check_file(self, filename, quiet=True):
        """
        <br>`param filename` string with path to JSON file
        <br>`return` boolean with state of JSON correctness
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
        <br>`param filename` path of file, where JSON will be saved
        <br>`param json_string` list or dict to save in file
        <br>`param quiet` boolean, suppress print to console
        <br>`param debug` boolean, needed for debugging
        <br>`return`
        """
        import json
        import sys
        from .file9 import File
        from .dict9 import Dict
        if debug:
            print("sys.argv[0] =", sys.argv[0])
            print(json_string)
        # try:
        File.wipe(filename)
        settings_json_text_io = open(filename, "w", encoding="utf8")
        try:
            json_string = Dict.all_keys_lambda(json_string, str)  # make sure that all keys is strings
        except TypeError:
            json_string = str(json_string)
        json.dump(json_string, settings_json_text_io, ensure_ascii=self.ensure_ascii)
        settings_json_text_io.close()
        if not quiet:
            print("JSON successfully saved")
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

    def _load_from_file(self, file_path, quiet=False, debug=False):
        """
        <br>`param filename` path of file, from load JSON
        <br>`param quiet` suppress print to console
        <br>`param debug` boolean, needed for debugging
        <br>`return`
        """
        import json
        import os
        if not os.path.isfile(file_path):
            from .file9 import File
            File.create(file_path)
            clean_json = {}
            self._save_to_file(file_path, clean_json)
        with open(file_path, encoding="utf8") as file_handle:
            try:
                json_string_in_memory = json.load(file_handle)
            except json.decoder.JSONDecodeError as e:
                from .file9 import File
                if File.read(file_path) == "":
                    json_string_in_memory = {}
                else:
                    raise e
        if not quiet:
            print("JSON successfully loaded")
        if debug:
            print(json_string_in_memory)
        return json_string_in_memory
