#! python3
# -*- coding: utf-8 -*-
"""Internal module with functions that work only in macOS."""
from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any, Optional, cast
else:
    def cast(_type, value):
        """Return value unchanged for runtime typing fallback."""
        return value
from .module import LazyModule, LazyProperty
__version__ = "0.3.1"
Print = LazyProperty(".print", "Print")
Dir = LazyProperty(".dir", "Dir")
Path = LazyProperty(".path", "Path")
Str = LazyProperty(".str", "Str")
OS = LazyProperty(".os", "OS")
Process = LazyProperty(".process", "Process")

backslash = "\\"


class macOS:  # pylint: disable=invalid-name, too-few-public-methods
    """Class with functions that work only in macOS."""

    def __init__(self, message: Optional[str] = None) -> None:
        self.message: Optional[str] = message
        self.title: str = "python3"
        self.subtitle: Optional[str] = None
        self.sound: Optional[str] = None

    def notify(
        self,
        title: str = "python3",
        subtitle: Optional[str] = None,
        sound: Optional[str] = None,
        debug: bool = False
    ) -> None:
        """Send a notification using stored message."""
        if self.message is None:
            raise ValueError("Message is not set")
        self.__class__.notification(self.message, title=title, subtitle=subtitle, sound=sound, debug=debug)

    def __call__(
        self,
        message: Optional[str] = None,
        title: Optional[str] = None,
        subtitle: Optional[str] = None,
        sound: Optional[str] = None,
        debug: bool = False
    ) -> None:
        """Send a notification using stored defaults."""
        if message is not None:
            self.message = message
        if title is not None:
            self.title = title
        if subtitle is not None:
            self.subtitle = subtitle
        if sound is not None:
            self.sound = sound
        self.notify(title=self.title, subtitle=self.subtitle, sound=self.sound, debug=debug)

    class OSAScript:  # pylint: disable=too-few-public-methods
        """Class with functions to work with osascript shell command."""

        @classmethod
        def quotes_escape(cls, string: str) -> str:
            """Try to escape quotes for AppleScript.

            <br>`param string` string input
            <br>`return` string with escaped symbols
            """
            quote_1 = '"'
            # quote_2 = "'"
            # if there any already escaped symbols:
            string = string.replace(backslash, backslash * 3)  # if there any other escaped symbols except quotes
            string = string.replace(backslash * 3 + quote_1,
                                    backslash * 2 + quote_1)  # removing one backslash, because it will added furthurer
            # string = string.replace(backslash*3+quote_2, backslash*2+quote_2)

            # usual quotes escape
            escaped_1 = backslash + quote_1
            # escaped_2 = backslash + quote_2
            string = string.replace(quote_1, escaped_1)
            # string = string.replace(quote_2, escaped_2)
            return string

    @classmethod
    def get_list_of_sounds(cls, verbose: bool = False) -> list[str]:
        """Print all sound names from current machine and user.

        <br>`param verbose` suppress print to console
        <br>`return` list of all sounds
        """
        global_sounds = Dir.list_of_files(Path.combine("System", "Library", "Sounds"))
        local_sounds = Dir.list_of_files(Path.combine("~", "Library", "Sounds"))
        if verbose:
            Print.debug("global sounds", repr(global_sounds), "local sounds", repr(local_sounds))
        return list(global_sounds) + list(local_sounds)

    @classmethod
    def notification(
        cls,
        message: str,
        title: Optional[str] = "python3",
        subtitle: Optional[str] = None,
        sound: Optional[str] = None,
        debug: bool = False
    ) -> None:
        """Create a notification with AppleScript.

        <br>`param message` string
        <br>`param title` string
        <br>`param subtitle` string
        <br>`param sound` string with sound name
        <br>`param list_of_sounds` boolean,
        <br>`return` None
        """
        # https://apple.stackexchange.com/questions/57412/how-can-i-trigger-a-notification-center-notification-from-an-a
        # pplescript-or-shel# - just AppleScript
        # better realizations:
        # advanced commandline tool - https://github.com/vjeantet/alerter
        # simpler commandline tool - https://github.com/vjeantet/alerter
        # commands = "display notification \"message\" with title \"title\" subtitle \"subtitle\" sound name \"Sosumi\""
        commands = "display notification " + Str.to_quotes(cls.OSAScript.quotes_escape(message))
        if title or subtitle:
            commands += " with "
            if title:
                commands += "title " + Str.to_quotes(cls.OSAScript.quotes_escape(title)) + " "
            if subtitle:
                commands += "subtitle " + Str.to_quotes(cls.OSAScript.quotes_escape(subtitle)) + " "
        if sound:
            commands += " sound name " + Str.to_quotes(cls.OSAScript.quotes_escape(sound))
        commands = cls.OSAScript.quotes_escape(commands)  # escaping quotes:
        commands = Str.to_quotes(commands)  # applescript to quotes
        command = " ".join(["osascript", "-e", commands])
        if debug:
            print(f"{command=}")
        OS.system(command)

    @classmethod
    def symlink(cls, real: str, symlink: str) -> None:
        """Create a symlink in macOS.

        <br>`param real` string, path to real folder or file, where be linked symlink
        <br>`param symlink` string, path to new symlink
        <br>`return` None
        """
        Process.start("ln", "-s", "'"+real+"'", "'"+symlink+"'")
