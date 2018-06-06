#! python3
# -*- coding: utf-8 -*-
"""Internal module to install requirements
"""
# pylint: disable=unused-import, exec-used, too-many-branches
import pkgutil
import importlib
import sys
import os
from commands.os8 import OS
from commands.pip8 import Pip
from commands.bench8 import get_Bench
from commands.print8 import Print
__version__ = "0.5.0"


def mine_import(module_name, objects=None, just_download=False, az=None):  # pylint: disable=invalid-name
    """Import module, if it doesn't installed, install it by pip
    :param module_name: string with module name
    :param objects: string of module parts needed to import
    :param just_download: disable import of module
    :param az: string with define variable name of module in globals
    :return: None
    """
    Pip.check_pip_installation()
    if module_name not in Pip.list_of_modules:
        # ##########RARE###########
        if module_name == "pyautogui":
            if OS.linux:
                if OS.is_python3:
                    os.system("apt-get install python-xlib")
                else:
                    os.system("apt-get install python3-Xlib")
            if OS.macos:
                for package in ["python" + OS.python_commandline_version + "-xlib",
                                "pyobjc-core", "pyobjc"]:
                    Pip.install(package)
                if OS.python_implementation == "pypy":
                    Print.debug("Yep, PyPy doesn't support pyobjc")
        if module_name in ["win32api", "win32con"]:
            Pip.install("pypiwin32")
        else:
        # ##########RARE###########
            Pip.install(module_name)
    if not just_download:
        def import_error():
            """Re-run whole script in last try to import installed module
            :return: None
            """
            import_fail_arg = "--import-fail"
            import_fail_count = 3
            if sys.argv.count(import_fail_arg) > import_fail_count:
                print('<<<<<<<<<<Some errors occured with importing "' + str(module_name) +
                      '", re-run script doesnt help, sorry about that>>>>>>>>>>')
                print('<<<<<<<<<<Trying to work without "' + str(module_name) + '">>>>>>>>>>')
            else:
                commands = ""
                if OS.windows and "py" not in str(sys.argv):
                    sys.argv.insert(0, "py")
                if ("-m" in sys.argv) and ("commands" not in sys.argv):  # if running with -m arg, "commands" doesn't go to sys.argv
                    sys.argv.append("commands")
                sys.argv.append(import_fail_arg)
                for arg in sys.argv:
                    commands += arg + " "
                commands = commands.rstrip(" ")
                print('<<<<<<<<<<Some errors occured with importing "' + str(module_name) +
                      '", trying to re-run script with parameters "' + commands + '">>>>>>>>>>')
                os.system(commands)
                sys.exit()
        try:
            if az and objects:
                if len(objects.split(",")) == 1:
                    globals()[az] = importlib.import_module(objects[0], package=module_name)
                print("mine_import doesn't support both attributes use 'az' and 'objects'")
                print("so only 'objects' will apply.")
                az = None
            if az:
                try:
                    globals()[az] = importlib.import_module(module_name)
                except ImportError as err:  # support for py3.4
                    print(err)
                    print("trying to import " + module_name + " in another way")
                    exec("import " + module_name + " as " + az, globals())
            elif objects:
                # import importlib  # todo better code
                # for object in objects.split(",")
                #     globals()[object] = importlib.import_module(name, package=module_name):
                # ### if " as " in object поделить и применить правильно, то есть имя назначить второе, а
                # ### импортировать из первого
                exec("from " + module_name + " import " + objects, globals())
            else:
                try:
                    globals()[module_name] = importlib.import_module(module_name)
                except ImportError as err:  # support for py3.4
                    print(err)
                    print("trying to import " + module_name + " in another way")
                    exec("import " + module_name, globals())
        except ImportError as err:  # support for py3.4
            import_error()


mine_import("termcolor")  # print_green_on_cyan = lambda x: cprint(x, 'green', 'on_cyan')
if OS.windows:
    mine_import("copypaste")
    mine_import("pyperclip", az="copypaste")
else:
    mine_import("copypaste")
if OS.display:
    if OS.python_implementation != "pypy":
        if OS.macos:
            mine_import("pyautogui")
        mine_import("paramiko")
    import tkinter
if OS.windows:
    if sys.version_info < (3, 6):
        mine_import("win_unicode_console")
    mine_import("win32api")
    mine_import("win32con")
    mine_import("termcolor")
mine_import("colorama")
