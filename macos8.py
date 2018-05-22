#! python3
# -*- coding: utf-8 -*-
__version__ = "0.0.1"


class macOS:
    class osascript:
        @staticmethod
        def quotes_escape(string):
            from .const8 import backslash
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
    def notification(cls, message, title="python3", subtitle=None, sound=None, list_of_sounds=False):
        # https://apple.stackexchange.com/questions/57412/how-can-i-trigger-a-notification-center-notification-from-an-applescript-or-shel# - just applescript
        # better realizations:
        # advanced commandline tool - https://github.com/vjeantet/alerter
        # simpler commandline tool - https://github.com/vjeantet/alerter
        # commands = "display notification \"message\" with title \"title\" subtitle \"subtitle\" sound name \"Sosumi\""
        from .str8 import Str
        from .
        commands = "display notification " + Str.to_quotes(cls.osascript.quotes_escape(message))
        if title or subtitle:
            commands += " with "
            if title:
                commands += "title " + Str.to_quotes(cls.osascript.quotes_escape(title)) + " "
            if subtitle:
                commands += "subtitle " + Str.to_quotes(cls.osascript.quotes_escape(subtitle)) + " "
        if sound:
            commands += " sound name " + Str.to_quotes(cls.osascript.quotes_escape(sound))
        commands = cls.osascript.quotes_escape(commands)  # escaping quotes:
        commands = Str.to_quotes(commands)  # applescript to quotes
        Process.start("osascript", "-e",
                      commands)  # f start(*arguments, new_window=False, debug=False, pureshell=False):
        if list_of_sounds:
            Print.debug("global sounds", Dir.list_of_files(Path.extend("System", "Library", "Sounds")), "local sounds",
                        Dir.list_of_files(Path.extend("~", "Library", "Sounds")))