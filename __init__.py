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
#    fix Str.get_integers!!!!!!!!!!!!!!!!!!
#    Console.get_output make ouptut even if exit status != 0
#    make tests for all
#    PEP8 check for all
#    !done! docstrings for all
#    new dir_c
#    Internal.rel update to reload all
#    Json.save update check of corectness save json with int keys in dict
#    !done!remove Time.rustime, change time format in log8
#    change all docstring to "Class with functions"
#    check docstrings for first Capitalized letter, dot at end, no more capitalized letter, for all parameters
#    check parameters to define types
#    fix OS.display
#    test all in linux
#    rewerite Str.diff_simple

# TODO version diff
#   export script as json?
#   compare json's?
#   save changes as commit message?

CLASSES_SPEED_TWEAKING = False
# CLASSES_SPEED_TWEAKING = True


def import_class(module_name, class_name, quiet=not CLASSES_SPEED_TWEAKING, reload=False):
    """Imports class from submodule.
    :param module_name: string with submodule name
    :param class_name: string with class name from submodule
    :param quiet: boolean suppress print to console
    :param reload: boolean, reloads loaded module
    :return: None
    """
    import importlib  # pylint: disable=unused-variable
    if reload:
        globals()[class_name] = eval("importlib.reload(commands." + module_name + ")." + class_name)  # pylint: disable=eval-used
    else:
        globals()[class_name] = eval("importlib.import_module('." + module_name + "', package='commands')."+class_name)  # pylint: disable=eval-used
    if not quiet:
        LOAD_TIME_BENCHMARK.end("class " + class_name + " loaded in", quiet_if_zero=True, start_immediately=True)


try:
    INITED_TIME = datetime.datetime.now()
    import_class("bench8", "get_Bench", quiet=True)
    if CLASSES_SPEED_TWEAKING:
        LOAD_TIME_BENCHMARK = get_Bench()  # pylint: disable=undefined-variable
        LOAD_TIME_BENCHMARK.fraction_digits = 4
        LOAD_TIME_BENCHMARK.time_start = START_TIME
        LOAD_TIME_BENCHMARK.end("init in", quiet_if_zero=True)
        LOAD_TIME_BENCHMARK.time_start = INITED_TIME
        LOAD_TIME_BENCHMARK.end("func get_Bench loaded in", quiet_if_zero=True, start_immediately=True)

    LIST_CLASSES = [{"module": "str8", "name": "Str"},
                    {"module": "os8", "name": "OS"},
                    {"module": "print8", "name": "Print"},
                    {"module": "console8", "name": "Console"},
                    {"module": "ssh8", "name": "Ssh"},
                    {"module": "file8", "name": "File"},
                    {"module": "locations8", "name": "Locations"},
                    {"module": "dir8", "name": "Dir"},
                    {"module": "path8", "name": "Path"},
                    {"module": "file8", "name": "File"},
                    {"module": "time8", "name": "Time"},
                    {"module": "json8", "name": "Json"},
                    {"module": "list8", "name": "List"},
                    {"module": "process8", "name": "Process"},
                    {"module": "dict8", "name": "Dict"},
                    {"module": "codegen8", "name": "Codegen"},
                    {"module": "log8", "name": "plog"},
                    {"module": "network8", "name": "Network"},
                    {"module": "bash8", "name": "Bash"},
                    {"module": "macos8", "name": "macOS"},
                    {"module": "windows8", "name": "Windows"},
                    {"module": "gui8", "name": "Gui"},
                    {"module": "tkinter8", "name": "Tkinter"},
                    {"module": "random8", "name": "Random"},
                    {"module": "wget8", "name": "Wget"},
                    {"module": "int8", "name": "Int"},
                    {"module": "cli8", "name": "CLI"},
                    {"module": "cs8", "name": "dirify"}, ]
    import commands.const8 as const8
    for object_name in dir(const8):
        if object_name[:1] != "_":
            LIST_CLASSES.append({"module": "const8", "name": object_name})
    for class_ in LIST_CLASSES:
        import_class(class_["module"], class_["name"])

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
                try:
                    import copypaste
                except ModuleNotFoundError:
                    from .installreq8 import copypaste
                copypaste.copy(string)

    if CLASSES_SPEED_TWEAKING:
        LOAD_TIME_BENCHMARK.end("class Internal loaded in", quiet_if_zero=True, start_immediately=True)

    class __build__:  # pylint: disable=too-few-public-methods, invalid-name
        build_json_file = Path.extend(Path.commands8(), "buildnumber.json")  # pylint: disable=undefined-variable
        try:
            build = Json.load(build_json_file, quiet=True)[0]  # pylint: disable=undefined-variable
        except:  # pylint: disable=bare-except
            build = "NaN"
        Json.save(build_json_file, [build + 1], quiet=True)  # pylint: disable=undefined-variable

    del INITED_TIME
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
    Print.debug("I tried my best to install dependencies, try to restart script, everything must be okay")
