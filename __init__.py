#! python3
# -*- coding: utf-8 -*-
import datetime
start_bench_no_bench = datetime.datetime.now()
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
# TODO version diff
#   todo export script as json?
#   todo compare jsons?
#   todo save changes as commit message?

FRACKING_classes_speed_tweaking = False
FRACKING_classes_speed_tweaking = True

try:
    bench_no_bench_init_time = datetime.datetime.now()
    from .bench8 import get_Bench
    if FRACKING_classes_speed_tweaking:
        LoadTimeBenchMark = get_Bench()
        LoadTimeBenchMark.fraction_digits = 4
        LoadTimeBenchMark.time_start = start_bench_no_bench
        LoadTimeBenchMark.end("init in", quiet_if_zero=True)
        LoadTimeBenchMark.time_start = bench_no_bench_init_time
        LoadTimeBenchMark.end("func get_Bench loaded in", quiet_if_zero=True, start_immideately=True)
    from .str8 import Str
    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Str loaded in", quiet_if_zero=True, start_immideately=True)  # python searching for that module in PATH
    from .os8 import OS
    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class OS loaded in", quiet_if_zero=True, start_immideately=True)
    from .print8 import Print
    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Print loaded in", quiet_if_zero=True, start_immideately=True)


    class Internal:
        @staticmethod
        def dir_c():
            """Print all functionality of commands8
            """
            raise NotImplementedError
            # commands.__dict__



        @staticmethod
        def rel(quiet=False):  # d reload commands8, if you use it not in REPL, activate quiet argument
          # d require additional line of code after reload if you import not entrie commands8
          # d you need manually add "from commands8 import *" to script/REPL
          # d if you import like "import commands8", additional line of code not needed
            import commands, importlib
            commands = importlib.reload(commands8)
            del commands
            string = "from commands import *"  # d you need to manually add this <<< string to code :(
            if not quiet:
                print('"'+string+'" copied to clipboard')
                try:
                    import copypaste
                except ModuleNotFoundError:
                    from .installreq8 import copypaste
                copypaste.copy(string)
                pass


    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Internal loaded in", quiet_if_zero=True, start_immideately=True)
    from .const8 import *
    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("imported constants in", quiet_if_zero=True, start_immideately=True)
    from .console8 import Console
    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Console loaded in", quiet_if_zero=True, start_immideately=True)
    from .ssh8 import Ssh
    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Ssh loaded in", quiet_if_zero=True, start_immideately=True)
    from .file8 import File
    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class File loaded in", quiet_if_zero=True, start_immideately=True)
    from .locations8 import Locations
    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Path loaded in", quiet_if_zero=True, start_immideately=True)
    from .dir8 import Dir
    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Path loaded in", quiet_if_zero=True, start_immideately=True)
    from .path8 import Path
    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Path loaded in", quiet_if_zero=True, start_immideately=True)
    from .file8 import File
    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class File loaded in", quiet_if_zero=True, start_immideately=True)
    from .time8 import Time
    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Time loaded in", quiet_if_zero=True, start_immideately=True)
    from .json8 import Json
    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Json loaded in", quiet_if_zero=True, start_immideately=True)
    from .list8 import List
    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class List loaded in", quiet_if_zero=True, start_immideately=True)
    from .process8 import Process
    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Process loaded in", quiet_if_zero=True, start_immideately=True)
    from .dict8 import Dict
    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Dict loaded in", quiet_if_zero=True, start_immideately=True)
    from .codegen8 import Codegen
    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Codegen loaded in", quiet_if_zero=True, start_immideately=True)
    from .log8 import plog
    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("func plog loaded in", quiet_if_zero=True, start_immideately=True)
    from .network8 import Network
    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Network loaded in", quiet_if_zero=True, start_immideately=True)
    from .bash8 import Bash
    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Bash loaded in", quiet_if_zero=True, start_immideately=True)
    if OS.macos:
        from .macos8 import macOS
    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class macOS loaded in", quiet_if_zero=True, start_immideately=True)
    from .gui8 import Gui
    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Gui loaded in", quiet_if_zero=True, start_immideately=True)
    from .tkinter8 import Tkinter
    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Tkinter loaded in", quiet_if_zero=True, start_immideately=True)
    if OS.windows:
        from .windows8 import Windows
    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Windows loaded in", quiet_if_zero=True, start_immideately=True)
    from .random8 import Random
    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Random loaded in", quiet_if_zero=True, start_immideately=True)
    from .wget8 import Wget
    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Wget loaded in", quiet_if_zero=True, start_immideately=True)
    from .int8 import Int
    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Int loaded in", quiet_if_zero=True, start_immideately=True)
    from .cli8 import CLI
    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class CLI loaded in", quiet_if_zero=True, start_immideately=True)

    LoadTimeBenchMark = get_Bench()
    LoadTimeBenchMark.time_start = start_bench_no_bench


    class __build__:
        build_json_file = Path.extend(Path.commands8(), "buildnumber.json")
        try:
            build = Json.load(build_json_file, quiet=True)[0]
        except:
            build = "NaN"
        Json.save(build_json_file, [build+1], quiet=True)


    LoadTimeBenchMark.end("commands8 v" + __version__ + "-'build'-" + str(__build__.build) + " loaded in")
except ModuleNotFoundError:
    import console.installreq8
    from .print8 import Print
    Print.debug("I tried my best to install dependencies, try to restart script, everything must be okay")
