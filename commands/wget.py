#! python3
# -*- coding: utf-8 -*-
"""Internal module wrapper to cli wget."""
from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any, Dict, Optional

from .module import LazyModule, LazyProperty

__version__ = "0.3.1"

os = LazyModule("os")
Console = LazyProperty(".console", "Console")
Dir = LazyProperty(".dir", "Dir")
Network = LazyProperty(".network", "Network")
Print = LazyProperty(".print", "Print")


class Wget:  # pylint: disable=too-few-public-methods
    """Class wrapper to cli wget."""

    def __init__(self, url: Optional[str] = None, output_filename: Optional[str] = None) -> None:
        self.url = url
        self.output_filename = output_filename
        self._defaults: Dict[str, Any] = {
            "verbose": False,
            "no_check_certificate": False,
            "wget_path": "wget",
            "timeout": None,
            "debug": False,
        }

    def __call__(self, url: Optional[str] = None, output_filename: Optional[str] = None, **kwargs: Any) -> str:
        """Shortcut to download using stored defaults/url/output."""
        if url:
            self.url = url
        if output_filename:
            self.output_filename = output_filename
        merged = {**self._defaults, **kwargs}
        return self.fetch(**merged)

    @classmethod
    def download(
        cls,
        url: str,
        output_filename: str,
        verbose: bool = False,
        no_check_certificate: bool = False,
        wget_path: str = "wget",
        timeout: Optional[float] = None,
        debug: bool = False
    ) -> str:
        """Wrap the wget CLI.

        <br>`param url` string, url to some file
        <br>`param output_filename` string, path to filename
        <br>`param verbose` boolean, suppress print to console
        <br>`return` output from wget if 'verbose' argument is False
        """
        output_filename = str(output_filename)
        arguments = [
                    '--header="Accept: text/html"',
                    '--user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) ' +
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3167.0 Safari/537.36"',
                    #  "--no-verbose",
                    f'--base="{Network.get_protocol_of_url(url)+Network.get_domain_of_url(url)}"'
                    ]
        if no_check_certificate:
            arguments.insert(1, "--no-check-certificate")

        commands = [wget_path, *arguments, url, "-O", output_filename, "--no-check-certificate"]
        if debug:
            Print.debug(" ".join(commands))
        if not Dir.exist(os.path.split(output_filename)[0]) and os.path.split(output_filename)[0]:
            Dir.create(os.path.split(output_filename)[0])
        try:
            output_raw = Console.get_output(commands, print_std=verbose, auto_disable_py_buffering=False,
                                            timeout=timeout, debug=debug)
            output = str(output_raw).strip(" \r\n")
            return output
        except FileNotFoundError as exception:
            raise OSError("wget executable not found; install wget and ensure it is on PATH") from exception
        # Another way to fix blocks by creating ~/.wgetrc file https://stackoverflow.com/a/34166756

    # Instance-friendly helper
    def fetch(self, output_filename: Optional[str] = None, **kwargs: Any) -> str:
        """Download using stored URL and defaults."""
        if not self.url:
            raise ValueError("URL is not set")
        target = output_filename or self.output_filename
        if not target:
            raise ValueError("Output filename is not set")
        return self.__class__.download(self.url, target, **kwargs)
