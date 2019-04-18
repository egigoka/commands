#! python3
# -*- coding: utf-8 -*-
"""Internal module wrapper to cli wget
"""
__version__ = "0.1.2"


class Wget:  # pylint: disable=too-few-public-methods
    """Class wrapper to cli wget
    """
    @staticmethod
    def download(url, output_filename, quiet=False, no_check_certificate=False):  # pylint: disable=inconsistent-return-statements
        """Wrapper to wget cli
        <br>`param url` string, url to some file
        <br>`param output_filename` string, path to filename
        <br>`param quiet` boolean, suppress print to console
        <br>`return` output from wget if 'quiet' argument is True
        """
        arguments = '--header="Accept: text/html" ' + \
                    '--user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) ' + \
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3167.0 Safari/537.36"'

        from .console9 import Console
        from .dir9 import Dir
        import os

        no_check_certificate_cli_arg = ""
        if no_check_certificate:
            no_check_certificate_cli_arg = "--no-check-certificate"

        command = f"wget {no_check_certificate_cli_arg} {url} -O {output_filename} {arguments}"
        if not Dir.exist(os.path.split(output_filename)[0]) and os.path.split(output_filename)[0]:
            Dir.create(os.path.split(output_filename)[0])
        try:
            return Console.get_output(command, print_std=not quiet)
        except FileNotFoundError as exception:
            raise OSError(exception, "install wget")
        # Another way to fix blocks by creating ~/.wgetrc file https://stackoverflow.com/a/34166756
