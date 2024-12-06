#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with JSON
"""
__version__ = "4.3.0"


class Json:
    """Class to work with JSON
    """

    def __init__(self, filename, quiet=True, ensure_ascii=False, debug=False):
        self.filename = filename
        self.ensure_ascii = ensure_ascii
        self.quiet = quiet
        self.debug = debug

        self.load(quiet=quiet)

    def __len__(self):
        return self.string.__len__()

    def __contains__(self, item):
        return self.string.__contains__(item)

    def __repr__(self):
        from .print9 import Print
        pretty = Print.prettify(self.string, quiet=True)
        return f"JSON '{self.filename}':\n{pretty}"

    __print__ = __repr__

    def pop(self, *args, **kwargs):
        output = self.string.pop(*args, **kwargs)
        return output

    def save(self, quiet=True, debug=False):
        """
        <br>`param quiet` boolean, suppress print to console
        <br>`param debug` boolean, needed for debugging
        <br>`return`
        """
        import json
        from .file9 import File
        if debug:
            print(self.string)
        # try:
        File.wipe(self.filename)
        with open(self.filename, "w", encoding="utf8") as settings_json_text_io:

            if isinstance(self.string, dict):
                from .dict9 import Dict
                self.string = Dict.all_keys_lambda(self.string, str)  # make sure that all keys is strings

            json.dump(self.string, settings_json_text_io, ensure_ascii=self.ensure_ascii)
        if not quiet:
            from .print9 import Print
            Print.multithread_safe("JSON successfully saved")

    def load(self, quiet=True, debug=False):
        """
        <br>`param quiet` suppress print to console
        <br>`param debug` boolean, needed for debugging
        <br>`return` None
        """
        import json
        import os
        if not os.path.isfile(self.filename):
            from .file9 import File
            try:
                File.create(self.filename)
                self.string = {}
                self.save()
            except FileExistsError:  # if file created while this code running
                pass
        with open(self.filename, encoding="utf8") as file_handle:
            try:
                self.string = json.load(file_handle)
            except json.decoder.JSONDecodeError as e:
                from .file9 import File
                if File.read(self.filename) == "":
                    self.string = {}
                else:
                    raise e
        if not quiet:
            print("JSON successfully loaded")
        if debug:
            print(self.string)


class JsonDict(Json):
    def __init__(self, filename, quiet=True, ensure_ascii=False, debug=False):
        Json.__init__(self=self, filename=filename, quiet=quiet, ensure_ascii=ensure_ascii, debug=debug)
        if not isinstance(self.string, dict):
            raise TypeError(f"Json file {filename} is not containing dict")

    def __getitem__(self, item):
        try:
            return self.string.__getitem__(item)
        except KeyError:
            info_string = f'''self={self}
self.string={self.string}")
item={item}
item not found!'''
            raise KeyError(info_string)

    def __setitem__(self, key, value):
        output = self.string.__setitem__(key, value)
        return output

    def __iter__(self):
        return self.string.__iter__()

    def __str__(self):
        from .print9 import Print
        return Print.prettify(self.string, quiet=True)

    def items(self):
        return self.string.items()

    def values(self):
        return self.string.values()

    def keys(self):
        return self.string.keys()

    def clear(self):
        return self.string.clear()


class JsonList(Json):
    __getitem__ = JsonDict.__getitem__
    __setitem__ = JsonDict.__setitem__

    def __init__(self, filename, quiet=True, ensure_ascii=False, debug=False):
        Json.__init__(self=self, filename=filename, quiet=quiet, ensure_ascii=ensure_ascii, debug=debug)
        if self.string == {}:  # if it's empty (new) file
            self.string = []
            self.save()
        if not isinstance(self.string, list):
            raise TypeError(f"Json file {filename} is not containing list")

    def __str__(self):
        from .print9 import Print
        return Print.prettify(self.string, quiet=True)

    def index(self, *args, **kwargs):
        output = self.string.index(*args, **kwargs)
        return output

    def append(self, element):
        self.string.append(element)

    def sort(self, *args, **kwargs):
        self.string.sort(*args, **kwargs)

    def clear(self, *args, **kwargs):
        self.string.clear(*args, **kwargs)
