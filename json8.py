#! python3
# -*- coding: utf-8 -*-
__version__ = "0.0.2"


class Json:
    @classmethod
    def check(cls, filename):
        try:
            cls.load(filename)
            return True
        except:  # any exception is False
            print("JSON is bad")
            return False

    @classmethod
    def save(cls, filename, jsonstring, quiet=False, debug=False):
        import json
        import sys
        from .file8 import File
        try:
            File.wipe(filename)
            settingsJsonTextIO = open(filename, "w")
            json.dump(jsonstring, settingsJsonTextIO)
            settingsJsonTextIO.close()
            if not quiet:
                print("JSON succesfull saved")
            if debug:
                print("sys.argv[0] =", sys.argv[0])
                print(jsonstring)
        except:
            from .path8 import Path
            raise IOError("error while saving JSON, try to repair script at path " +
                          Path.full(sys.argv[0]))
        json_test_string = cls.load(filename, quiet=True)
        if jsonstring != json_test_string:
            from .path8 import Path
            from .print8 import Print
            Print.debug("jsonstring_to_save", jsonstring, "json_test_string_from_file", json_test_string)
            raise IOError("error while saving JSON, try to repair script at path " +
                          Path.full(sys.argv[0]))  # exception

    @classmethod
    def load(cls, filename, quiet=False, debug=False):
        import json, os
        try:
            if not os.path.isfile(filename):
                from .file8 import File
                File.create(filename)
                cleanjson = {}
                cls.save(filename, cleanjson)
            settingsJsonTextIO = open(filename)
            jsonStringInMemory = json.load(settingsJsonTextIO)
            settingsJsonTextIO.close()
            if not quiet:
                print("JSON succesfull loaded")
            if debug:
                print(jsonStringInMemory)
            return jsonStringInMemory
        except:
            import sys
            from .path8 import Path
            raise IOError("error while loading JSON, try to repair script at path " +
                          Path.full(sys.argv[0]))
