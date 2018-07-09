#! python3
# -*- coding: utf-8 -*-
"""This is kinda tiny framework? Idk.
I learn Python by creating this.
Also I have some memory issues, so programming with this library and fixing it help me to learn programming.
Otherwise I every time search how to do some thing and just copy-paste it without understanding and memorizing.
"""
import datetime
START_TIME = datetime.datetime.now()
__version__ = "9.0.0-prealpha"
# TODO for 9.0.0 release:
#    !done! OS class vars not strings, but booleans
#    !done! lazy load for all modules
#    !done! all submodules lazy load
#    !done! fix Str.get_integers!!!!!!!!!!!!!!!!!!
#    !done! remove Time.rustime, change time format in log8
#    !done! docstrings for all
#    make tests for all
#    PEP8 check for all
#    Console.get_output make output even if exit status != 0
#    new dir_c
#    Internal.rel update to reload all
#    Json.save update check of corectness save json with int keys in dict
#    change all docstring to "Class with functions"
#    check docstrings for first Capitalized letter, dot at end, no more capitalized letter, for all parameters
#    check parameters to define types
#    fix OS.display
#    test all in linux
#    rewerite Str.diff_simple
#    Path.expand bug with "." and ".." in windows
#    do better benchmarking of commands import
#    Json throw exceptions

# TODO version diff
#   export script as json?
#   compare json's?
#   save changes as commit message?

CLASSES_SPEED_TWEAKING = False
# CLASSES_SPEED_TWEAKING = True

try:
    from .bench8 import get_Bench
    if CLASSES_SPEED_TWEAKING:
        LOAD_TIME_BENCHMARK = get_Bench()
        LOAD_TIME_BENCHMARK.fraction_digits = 4
    from .str8 import Str
    from .os8 import OS
    from .print8 import Print
    from .console8 import Console
    from .ssh8 import Ssh
    from .file8 import File
    from .locations8 import Locations
    from .dir8 import Dir
    from .path8 import Path
    from .file8 import File
    from .time8 import Time
    from .json8 import Json
    from .list8 import List
    from .process8 import Process
    from .dict8 import Dict
    from .codegen8 import Codegen
    from .log8 import plog
    from .network8 import Network
    from .bash8 import Bash
    from .macos8 import macOS
    from .windows8 import Windows
    from .gui8 import Gui
    from .tkinter8 import Tkinter
    from .random8 import Random
    from .wget8 import Wget
    from .int8 import Int
    from .cli8 import CLI
    from .cs8 import dirify
    from .const8 import backslash, newline, newline2, ruble

    class Internal:
        """Internal class with internal functions
        """

        @staticmethod
        def dir_c():
            """Print all functionality of commands8
            """
            raise NotImplementedError
            # commands.__dict__

        @staticmethod
        def rel(quiet=False):
            """Reload commands8, if you use it not in REPL, activate quiet argument require additional line of code
            after reload if you import not entrie commands8 you need manually add "from commands8 import *" to
            script/REPL if you import like "import commands", additional line of code not needed
            :param quiet: boolean, True suppress print to terminal and interaction with clipboard
            :return: None
            """
            import importlib
            import commands  # pylint: disable=import-self, redefined-outer-name

            commands = importlib.reload(commands)

            del commands
            string = "from commands import *"  # d you need to manually add this <<< string to code :(
            if not quiet:
                print('"' + string + '" copied to clipboard')
                import copypaste
                copypaste.copy(string)

    class __build__:  # pylint: disable=too-few-public-methods, invalid-name
        build_py_file = Path.extend(Path.commands8(), "buildnumber.py")  # pylint: disable=undefined-variable
        try:
            from .buildnumber import build
        except ModuleNotFoundError:
            build = -1
        build += 1
        File.write(build_py_file, f"#! python3{newline2}# -*- coding: utf-8 -*-{newline2}build = {build}")


    del CLASSES_SPEED_TWEAKING
    LOAD_TIME_BENCHMARK = get_Bench()  # pylint: disable=undefined-variable
    LOAD_TIME_BENCHMARK.time_start = START_TIME
    LOAD_TIME_BENCHMARK.end("commands v" + __version__ + "-'build'-" + str(__build__.build) + " loaded in")
    del START_TIME
    del LOAD_TIME_BENCHMARK
except ModuleNotFoundError as err:
    print(err)
    import commands.installreq8
    from .print8 import Print
    Print.debug("I tried my best to install dependencies, try to restart script, everything must be okay...")
