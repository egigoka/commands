#! python3
# -*- coding: utf-8 -*-
"""Internal module to simplify work with git
"""
# pylint: disable=unused-wildcard-import, wildcard-import
__version__ = "2.2.0"


def get_name_of_repo():
    """Return mine name of repo
    <br>`return` string, name of repo
    """
    import os
    from .path9 import Path
    if Path.working().split(os.sep)[-1] in ["t", "term"]:
        return "test"
    return Path.working().split(os.sep)[-1]


class Git:
    """Class to simplify work with git, wrapper for cli git
    """
    @classmethod
    def add(cls, what, verbose=False):
        """Adds files to next commit
        <br>`param what` string, adding files
        <br>`return` None
        """
        from .console9 import Console
        Console.get_output("git", "add", what, print_std=verbose)

    @classmethod
    def commit(cls, message=None, verbose=False):
        """Commit all added changes
        <br>`param message` string, message of commit
        <br>`return` None
        """
        from .bash9 import Bash
        from .console9 import Console

        commands = ["git", "commit"]
        if message:
            commands.append("-m")
            commands.append(Bash.argument_escape(message))
        Console.get_output(commands, print_std=verbose)

    @classmethod
    def push(cls, path, upstream=False, verbose=False):
        """Push commits to 'path' repo
        <br>`param path` string, path of repo
        <br>`param upstream` boolean, if True, adding argument '-u' to git
        <br>`return` None
        """
        from .console9 import Console

        commands = ["git", "push"]
        if upstream:
            commands.append("-u")
        commands.append(path)
        Console.get_output(commands, print_std=verbose)

    @classmethod
    def update(cls, message, path="https://github.com/egigoka/" + get_name_of_repo() + ".git", verbose=False):
        """Automation to my git upload
        <br>`param message` string, commit message
        <br>`param path` string, path to repo
        <br>`return` None
        """
        cls.add(".", verbose=verbose)
        cls.commit(message, verbose=verbose)
        cls.push(path, upstream=True, verbose=verbose)
