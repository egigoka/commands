#! python3
# -*- coding: utf-8 -*-
"""Internal module wrapper to cli wget
"""
__version__ = "0.2.15"


class Wget:  # pylint: disable=too-few-public-methods
    """Class wrapper to cli wget
    """
    @classmethod
    def download(cls, url, output_filename, quiet=False, no_check_certificate=False, wget_path="wget", timeout=None):  # pylint: disable=inconsistent-return-statements
        """Wrapper to wget cli
        <br>`param url` string, url to some file
        <br>`param output_filename` string, path1 to filename
        <br>`param quiet` boolean, suppress print to console
        <br>`return` output from wget if 'quiet' argument is True
        """
        import os
        from .network9 import Network
        from .console9 import Console
        from .dir9 import Dir
        arguments = [
                    '--header="Accept: text/html"',
                    '--user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) ' + \
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3167.0 Safari/537.36"',
                    #"--no-verbose",
                    f'--base="{Network.get_protocol_of_url(url)+Network.get_domain_of_url(url)}"'
                    ]
        if no_check_certificate:
            arguments.insert(1, "--no-check-certificate")

        commands = [wget_path, *arguments, url, "-O", output_filename, "--no-check-certificate"]
        if not Dir.exist(os.path.split(output_filename)[0]) and os.path.split(output_filename)[0]:
            Dir.create(os.path.split(output_filename)[0])
        try:
            output = Console.get_output(commands, print_std=not quiet, auto_disable_py_buffering=False, timeout=timeout).strip(" \r\n")
            return output
        except FileNotFoundError as exception:
            if wget_path == "wget":
                from .path9 import Path
                from .os9 import OS
                wget_exec_name = "wget"
                if OS.windows:
                    wget_exec_name += ".exe"
                return cls.download(url=url, output_filename=output_filename, quiet=quiet, no_check_certificate=no_check_certificate,
                                    wget_path=Path.combine(Path.commands(), "res", wget_exec_name))
            raise OSError(exception, "install wget")
        # Another way to fix blocks by creating ~/.wgetrc file https://stackoverflow.com/a/34166756
