#! python3
# -*- coding: utf-8 -*-
"""Internal module with functions to work with pip
"""
__version__ = "0.1.7"


class Pip:
    """Aliases to work with pip.
    """
    @staticmethod
    def main(list_of_args):
        """
        It's alias of pip.main function, it needed, because pip10 remove public API
        <br>`param list_of_args` must be list, same arguments as pip
        <br>`return` same as alias
        """
        try:
            from pip import main as pip_main
        except ImportError:
            from pip._internal import main as pip_main
        return pip_main(list_of_args)

    @classmethod
    def install(cls, *module_names, upgrade=False, uninstall=False):
        """
        Alias to 'pip install'
        <br>`param module_names`
        <br>`param upgrade` boolean, if True, "--upgrade" argument will pass to pip
        <br>`param uninstall` boolean, if True, "uninstall", "-y" arguments will pass to pip
        <br>`return` None
        """
        import time
        from .list9 import List
        commands = ["install"]
        if uninstall:
            commands = ["uninstall", "-y"]
        elif upgrade:
            commands.append("--upgrade")
        commands.append(module_names)
        cls.main(List.flatterize(commands))
        time.sleep(0.5)
        cls._update_list_of_modules()

    @classmethod
    def uninstall(cls, *module_names):
        """
        Alias to Pip.install with True passed to uninstall argument
        <br>`param module_names`
        <br>`return` None
        """
        cls.install(*module_names, uninstall=True)

    @classmethod
    def check_pip_installation(cls):
        """
        Checks pip installation on Linux, if it hasn't, tries to install it with apt-get
        <br>`return` None
        """
        if "pip" not in cls.list_of_modules:
            from .os9 import OS
            if OS.linux:
                import os
                os.system("sudo apt-get install python" + OS.python_commandline_version + "-pip")

    @classmethod
    def update_all_packages(cls):
        """
        Update _all_ installed packages at once
        <br>`return` None
        """
        from .str9 import Str
        from .console9 import Console
        packages = Str.nl(Console.get_output("pip list"))
        packages_names = []
        for package in packages[3:]:
            if ("Package" not in package) and ("---" not in package) and package != "":
                packages_names.append(Str.get_words(package)[0])
        from .print9 import Print
        Print.debug(packages_names)
        cls.install(*packages_names, upgrade=True)

    list_of_modules = []

    @classmethod
    def _update_list_of_modules(cls):
        """
        Internal method. Updates internal list of modules.
        <br>`return` None
        """
        import pkgutil
        cls.list_of_modules = []
        for item in pkgutil.iter_modules():
            cls.list_of_modules.append(item[1])


Pip._update_list_of_modules()  # pylint: disable=protected-access
