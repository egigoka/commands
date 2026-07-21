#! python3
# -*- coding: utf-8 -*-
"""Tiny framework notes.

This is kinda tiny framework? IDK.
I learn Python by creating this.
Also, I have some memory issues, so programming with this library and fixing it help me to learn programming.
Otherwise, I every time search how to do something and just copy-paste it without understanding and memorizing.
"""

from .module import LazyModule, LazyProperty
Bench = LazyProperty(".bench", "Bench")
Str = LazyProperty(".str", "Str")
OS = LazyProperty(".os", "OS")
Print = LazyProperty(".print", "Print")
__Print = LazyProperty(".print", "__Print")
Console = LazyProperty(".console", "Console")
Ssh = LazyProperty(".ssh", "Ssh")
File = LazyProperty(".file", "File")
Dir = LazyProperty(".dir", "Dir")
Path = LazyProperty(".path", "Path")
Time = LazyProperty(".time", "Time")
Json = LazyProperty(".json", "Json")
JsonDict = LazyProperty(".json", "JsonDict")
JsonList = LazyProperty(".json", "JsonList")
List = LazyProperty(".list", "List")
Process = LazyProperty(".process", "Process")
Dict = LazyProperty(".dict", "Dict")
ImDict = LazyProperty(".dict", "ImDict")
Network = LazyProperty(".network", "Network")
Bash = LazyProperty(".bash", "Bash")
macOS = LazyProperty(".macos", "macOS")
Mouse = LazyProperty(".mouse", "Mouse")
Windows = LazyProperty(".windows", "Windows")
Gui = LazyProperty(".gui", "Gui")
Tkinter = LazyProperty(".tkinter", "Tkinter")
Random = LazyProperty(".random", "Random")
Wget = LazyProperty(".wget", "Wget")
Int = LazyProperty(".int", "Int")
CLI = LazyProperty(".cli", "CLI")
Base64 = LazyProperty(".base64", "Base64")
dirify = LazyProperty(".funcs", "dirify")
multiple = LazyProperty(".funcs", "multiple")
copy = LazyProperty(".funcs", "copy")
paste = LazyProperty(".funcs", "paste")
q = LazyProperty(".funcs", "q")
exit = LazyProperty(".funcs", "exit")
ID = LazyProperty(".id", "ID")
Git = LazyProperty(".git", "Git")
TSQL = LazyProperty(".tsql", "TSQL")
Cache = LazyProperty(".cache", "Cache")
CachedFunction = LazyProperty(".cache", "CachedFunction")
MyThread = LazyProperty(".threading", "MyThread")
Threading = LazyProperty(".threading", "Threading")
Lock = LazyProperty(".threading", "Lock")
Bytes = LazyProperty(".bytes", "Bytes")
GIV = LazyProperty(".giv", "GIV")
Archive = LazyProperty(".archive", "Archive")
FFMpeg = LazyProperty(".ffmpeg", "FFMpeg")
Keyboard = LazyProperty(".keyboard", "Keyboard")
Obj = LazyProperty(".obj", "Obj")
Screen = LazyProperty(".screen", "Screen")
Video = LazyProperty(".video", "Video")
Audio = LazyProperty(".audio", "Audio")
__version__ = LazyProperty("._version", "__version__")
add_instance_shortcuts = LazyProperty("._instance", "add_instance_shortcuts")
backslash = LazyProperty(".const", "backslash")
newline = LazyProperty(".const", "newline")
newline2 = LazyProperty(".const", "newline2")
ruble = LazyProperty(".const", "ruble")
rtl = LazyProperty(".const", "rtl")
KiB = LazyProperty(".const", "KiB")
MiB = LazyProperty(".const", "MiB")
GiB = LazyProperty(".const", "GiB")
TiB = LazyProperty(".const", "TiB")

# Enable instance-level shortcuts for classmethod-heavy modules to allow short, REPL-friendly syntax.
add_instance_shortcuts(
    Bench, Str, OS, __Print, Console, Ssh, Dir, Path, Time, Json, JsonDict, JsonList,
    List, Process, Dict, ImDict, Network, Bash, macOS, Mouse, Windows, Gui, Tkinter,
    Random, Wget, Int, CLI, Base64, ID, Git, TSQL, Cache, CachedFunction, Bytes, GIV,
    Archive, FFMpeg, Keyboard, Obj, Screen, Video, Audio, MyThread, Threading, Lock
)
