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

from .bench9 import Bench
if CLASSES_SPEED_TWEAKING:
    CLASSES_BENCHMARK = Bench(fraction_digits=4)
from .str9 import Str
from .os9 import OS
from .print9 import Print
from .console9 import Console
from .ssh9 import Ssh
from .file9 import File
from .locations9 import Locations
from .dir9 import Dir
from .path9 import Path
from .file9 import File
from .time9 import Time
from .json9 import Json
from .list9 import List
from .process9 import Process
from .dict9 import Dict
from .codegen9 import Codegen
from .log9 import plog
from .network9 import Network
from .bash9 import Bash
from .macos9 import macOS
from .windows9 import Windows
from .gui9 import Gui
from .tkinter9 import Tkinter
from .random9 import Random
from .wget9 import Wget
from .int9 import Int
from .cli9 import CLI
from .funcs9 import dirify
from .zip9 import Zip, Unzip
from .const9 import backslash, newline, newline2, ruble
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
