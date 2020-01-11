#! python3
# -*- coding: utf-8 -*-
"""Internal module with functions that works only in macOS
"""
__version__ = "0.2.4"


class macOS:  # pylint: disable=invalid-name, too-few-public-methods
    """Class with functions that works only in macOS
    """
    class OSAScript:  # pylint: disable=too-few-public-methods
        """Class with function to work with osascript shell command
        """
        @staticmethod
        def quotes_escape(string):
            """Trying to escape quotes to puch them through AppleScript
            <br>`param string` string input
            <br>`return` string with escaped symbols
            """
            from .const9 import backslash
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
    def get_list_of_sounds(cls, quiet=False):
        """Print all sound names from current machine and user
        <br>`param quiet` suppress print to console
        <br>`return` list of all sounds
        """
        from .print9 import Print
        from .dir9 import Dir
        from .path9 import Path
        global_sounds = Dir.list_of_files(Path.combine("System", "Library", "Sounds"))
        local_sounds = Dir.list_of_files(Path.combine("~", "Library", "Sounds"))
        if not quiet:
            Print.debug("global sounds", global_sounds, "local sounds", local_sounds)
        return global_sounds + local_sounds

    @classmethod
    def notification(cls, message, title="python3", subtitle=None, sound=None):
        """Create notification with AppleScript
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
        from .str9 import Str
        from .process9 import Process
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
        Process.start("osascript", "-e",
                      commands)  # f start(*arguments, new_window=False, debug=False, pureshell=False):

    @staticmethod
    def symlink(real, symlink):
        """Creates symlink in macOS
        <br>`param real` string, path to real folder or file, where be linked symlink
        <br>`param symlink` string, path to new symlink
        <br>`return` None
        """
        from .process9 import Process
        Process.start("ln", "-s", "'"+real+"'", "'"+symlink+"'")

