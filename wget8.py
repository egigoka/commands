#! python3
# -*- coding: utf-8 -*-
"""Internal module wrapper to cli wget
"""
__version__ = "0.0.5"


class Wget:  # pylint: disable=too-few-public-methods
    """Class wrapper to cli wget
    """
    @staticmethod
    def download(url, output_filename, quiet=False):  # pylint: disable=inconsistent-return-statements
        """Wrapper to wget cli
        :param url: string, url to some file
        :param output_filename: string, path to filename
        :param quiet: boolean, suppress print to console
        :return: output from wget if 'quiet' argument is True
        """
        arguments = '--header="Accept: text/html" ' + \
                    '--user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) ' + \
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3167.0 Safari/537.36"'
        if quiet:
            from .console8 import Console
            command = "wget '" + url + "' -O " + output_filename + " " + arguments
            return Console.get_output(command)
        else:
            from .process8 import Process
            from .const8 import backslash
            url = url.replace("&", backslash + "&")
            Process.start("wget", url, "-O", output_filename, arguments, pureshell=True)
        # Another way to fix blocks by creating ~/.wgetrc file https://stackoverflow.com/a/34166756
