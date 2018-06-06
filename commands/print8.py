#! python3
# -*- coding: utf-8 -*-
"""Internal module with functions for print to console.
"""
__version__ = "0.4.2"


class Print:
    """Class with functions for print to console.
    """
    @staticmethod
    def debug(*strings, raw=False):
        """More notable print, used only for debugging
        :param strings: strings, prints separately
        :param raw: print representation of raw strings
        :return:
        """
        from .console8 import Console
        line = "-" * Console.width()
        print("<<<Debug sheet:>>>")
        for str_ in strings:
            print(line, end="")
            if raw:
                print(repr(str_))
            else:
                print(str_)
            print(line)
        print("<<<End of debug sheet>>>")

    @staticmethod
    def rewrite(*strings, sep=" "):
        """Print rewritable string. note, that you need to rewrite string to remove previous characters
        :param strings: strings, work as builtin print()
        :param sep: sep as builtin print(sep)
        :return:
        """
        from .os8 import OS
        from .console8 import Console
        line = " " * Console.width()
        if OS.windows:  # windows add symbol to end of string :(
            line = line[:-1]
        print(line, end="\r")
        print(*strings, sep=sep, end="\r")

    @staticmethod
    def prettify(object_, indent=4, quiet=False):
        """Pretty print of list, dicts, tuples
        :param object_: list|dict|tuple
        :param indent: int, indent to new nested level
        :param quiet: boolean, suppress print to console
        :return: string, from pprint.pformat
        """
        import pprint
        pretty_printer = pprint.PrettyPrinter(indent=indent)
        if not quiet:
            pretty_printer.pprint(object_)
        return pretty_printer.pformat(object=object_)

    colorama_inited = False

    @classmethod
    def colored(cls, *strings, attributes=None, end="\n", sep=" "):
        """Wrapper for tkinter.cprint, added some smartness :3
        Usage: Print.colored("text1", "text2", "red") or cls.colored("text", "text2", "red", "on_white").
        You can pick colors from termcolor.COLORS, highlights from termcolor.HIGHLIGHTS.
        :param strings: strings, work as builtin print()
        :param attributes: list of attributes, going to tkinter.cprint(attrs) argument
        :param end: string, same end, as builtin print(end)
        :param sep: string, same end, as builtin print(sep)
        :return: None
        """
        try:
            import termcolor
        except ImportError:
            from .installreq8 import termcolor
        from .os8 import OS
        if OS.windows:
            try:
                import colorama
            except ImportError:
                from .installreq8 import colorama
            colorama.init()
        # check for colors in input
        highlight = None
        color = None
        color_args = 0
        if len(strings) >= 3:
            if strings[-1] in termcolor.HIGHLIGHTS:
                highlight = strings[-1]
                color_args += 1
                if strings[-2] in termcolor.COLORS:
                    color = strings[-2]
                color_args += 1
        elif len(strings) >= 2:
            if strings[-1] in termcolor.COLORS:
                color = strings[-1]
                color_args += 1
            elif strings[-1] in termcolor.HIGHLIGHTS:
                highlight = strings[-1]
                color_args += 1
        # create single string to pass it into termcolor
        string = ""
        strings = strings[:-color_args]
        if len(strings) > 1:
            for substring in strings[:-1]:  # все строки добавляются в основную строку с сепаратором
                string += substring + sep
            string += strings[-1]  # последняя без сепаратора
        else:  # if there only one object
            string = strings[0]
        # run termcolor
        termcolor.cprint(string, color=color, on_color=highlight, attrs=attributes, end=end)