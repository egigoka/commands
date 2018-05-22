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
    # !done! OS class vars not strings, but booleans
    # !done! lazy load for all modules
    # !done! all submodules lazy load
    # fix Time.rustime without cyrillic_support
    # Console.get_output make ouptut even if exit status != 0
    # make tests for all
    # PIP8 check for all
    # docstrings for all
    # new dir_c
    # Internal.rel update to reload all
# TODO version diff
#   todo export script as json?
#   todo compare jsons?
#   todo save changes as commit message?

CLASSES_SPEED_TWEAKING = False
CLASSES_SPEED_TWEAKING = True


def import_class(module_name, class_name, quiet=False):
    import importlib  # pylint: disable=unused-variable
    globals()[class_name] = eval("importlib.import_module('." + module_name + "', package='commands')." + class_name) # pylint: disable=eval-used
    if CLASSES_SPEED_TWEAKING and not quiet:
        LOAD_TIME_BENCHMARK.end("class " + class_name + " loaded in", quiet_if_zero=True, start_immideately=True)


try:
    INITED_TIME = datetime.datetime.now()
    import_class("bench8", "get_Bench", quiet=True)
    if CLASSES_SPEED_TWEAKING:
        LOAD_TIME_BENCHMARK = get_Bench()  # pylint: disable=undefined-variable
        LOAD_TIME_BENCHMARK.fraction_digits = 4
        LOAD_TIME_BENCHMARK.time_start = START_TIME
        LOAD_TIME_BENCHMARK.end("init in", quiet_if_zero=True)
        LOAD_TIME_BENCHMARK.time_start = INITED_TIME
        LOAD_TIME_BENCHMARK.end("func get_Bench loaded in", quiet_if_zero=True, start_immideately=True)

    import_class("str8", "Str")
    # python searching for that module in PATH
    import_class("os8", "OS")
    import_class("print8", "Print")
    import_class("console8", "Console")
    import_class("ssh8", "Ssh")
    import_class("file8", "File")
    import_class("locations8", "Locations")
    import_class("dir8", "Dir")
    import_class("path8", "Path")
    import_class("file8", "File")
    import_class("time8", "Time")
    import_class("json8", "Json")
    import_class("list8", "List")
    import_class("process8", "Process")
    import_class("dict8", "Dict")
    import_class("codegen8", "Codegen")
    import_class("log8", "plog")
    import_class("network8", "Network")
    import_class("bash8", "Bash")
    if OS.macos:  # pylint: disable=undefined-variable
        import_class("macos8", "macOS")
    elif OS.windows:  # pylint: disable=undefined-variable
        import_class("windows8", "Windows")
    import_class("gui8", "Gui")
    import_class("tkinter8", "Tkinter")
    import_class("random8", "Random")
    import_class("wget8", "Wget")
    import_class("int8", "Int")
    import_class("cli8", "CLI")
    from .const8 import *  # pylint: disable=wildcard-import
    if CLASSES_SPEED_TWEAKING:
        LOAD_TIME_BENCHMARK.end("imported constants in", quiet_if_zero=True, start_immideately=True)
    LOAD_TIME_BENCHMARK = get_Bench()  # pylint: disable=undefined-variable
    LOAD_TIME_BENCHMARK.time_start = START_TIME


    class Internal:
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
            globals()["Wget"] = eval("importlib.reload(commands.wget8).Wget")  # pylint: disable=eval-used
            commands = importlib.reload(commands)

            del commands
            string = "from commands import *"  # d you need to manually add this <<< string to code :(
            if not quiet:
                print('"'+string+'" copied to clipboard')
                try:
                    import copypaste
                except ModuleNotFoundError:
                    from .installreq8 import copypaste
                copypaste.copy(string)


    if CLASSES_SPEED_TWEAKING:
        LOAD_TIME_BENCHMARK.end("class Internal loaded in", quiet_if_zero=True, start_immideately=True)

    class __build__:  # pylint: disable=too-few-public-methods, invalid-name
        build_json_file = Path.extend(Path.commands8(), "buildnumber.json")  # pylint: disable=undefined-variable
        try:
            build = Json.load(build_json_file, quiet=True)[0]  # pylint: disable=undefined-variable
        except:  # pylint: disable=bare-except
            build = "NaN"
        Json.save(build_json_file, [build+1], quiet=True)  # pylint: disable=undefined-variable

    del START_TIME
    del INITED_TIME
    del CLASSES_SPEED_TWEAKING
    LOAD_TIME_BENCHMARK.end("commands8 v" + __version__ + "-'build'-" + str(__build__.build) + " loaded in")
    del LOAD_TIME_BENCHMARK
except ModuleNotFoundError:
    import commands.installreq8
    from .print8 import Print
    Print.debug("I tried my best to install dependencies, try to restart script, everything must be okay")
