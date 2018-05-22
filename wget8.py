#! python3
# -*- coding: utf-8 -*-
__version__ = "0.0.3"


class Wget:
    @staticmethod
    def download(url, output, quiet=False):  # just wrapper for commandline wget
        arguments = '--header="Accept: text/html" ' + \
                    '--user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) ' + \
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3167.0 Safari/537.36"'
        if quiet:
            from .console8 import Console
            command = "wget '" + url + "' -O " + output + " " + arguments
            return Console.get_output(command)
        else:
            from .process8 import Process
            from .const8 import backslash
            url = url.replace("&", backslash + "&")
            Process.start("wget", url, "-O", output, arguments, pureshell=True)
        # Another way to fix blocks by creating ~/.wgetrc file https://stackoverflow.com/a/34166756
