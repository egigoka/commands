#! python3
# -*- coding: utf-8 -*-
"""This is kinda tiny framework? Idk.
I learn Python by creating this.
Also I have some memory issues, so programming with this library and fixing it help me to learn programming.
Otherwise I every time search how to do some thing and just copy-paste it without understanding and memorizing.
"""
import datetime
START_TIME = datetime.datetime.now()

CLASSES_SPEED_TWEAKING = False
# CLASSES_SPEED_TWEAKING = True

from .bench8 import Bench
if CLASSES_SPEED_TWEAKING:
    CLASSES_BENCHMARK = Bench(fraction_digits=4)
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
from ._version import __version__

class Internal:
    """Internal class with internal functions
    """

    @staticmethod
    def help():
        """Print all functionality of commands8
        """
        raise NotImplementedError
        # commands.__dict__

if CLASSES_SPEED_TWEAKING:
    del CLASSES_BENCHMARK
del CLASSES_SPEED_TWEAKING
LOAD_TIME_BENCHMARK = Bench(f"commands {__version__} loaded in", time_start=START_TIME)
LOAD_TIME_BENCHMARK.end()
del START_TIME
del LOAD_TIME_BENCHMARK
