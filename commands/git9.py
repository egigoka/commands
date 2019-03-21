#! python3
# -*- coding: utf-8 -*-
"""Internal module to simplify work with git
"""
# pylint: disable=unused-wildcard-import, wildcard-import
import sys
from commands.path9 import Path
from commands.process9 import Process
from commands.bash9 import Bash
from commands.file9 import File
from commands.str9 import Str
__version__ = "2.0.1"


def get_name_of_repo():
    """Return mine name of repo
    <br>`return` string, name of repo
    """
    import os
    if Path.working().split(os.sep)[-1] in ["t", "term"]:
        return "test"
    return Path.working().split(os.sep)[-1]


class Git:
    """Class to simplify work with git, wrapper for cli git
    """
    @classmethod
    def add(cls, what):
        """Adds files to next commit
        <br>`param what` string, adding files
        <br>`return` None
        """
        Process.start("git", "add", what)

    @classmethod
    def commit(cls, message=None):
        """Commit all added changes
        <br>`param message` string, message of commit
        <br>`return` None
        """
        commands = ["git", "commit"]
        if message:
            commands.append("-m")
            commands.append(Bash.argument_escape(message))
        Process.start(commands)

    @classmethod
    def push(cls, path, upstream=False):
        """Push commits to 'path' repo
        <br>`param path` string, path of repo
        <br>`param upstream` boolean, if True, adding argument '-u' to git
        <br>`return` None
        """
        commands = ["git", "push"]
        if upstream:
            commands.append("-u")
        commands.append(path)
        Process.start(commands)

    @classmethod
    def update(cls, message, path="https://github.com/egigoka/" + get_name_of_repo() + ".git"):
        """Automatization to mine git upload
        <br>`param message` string, commit message
        <br>`param path` string, path to repo
        <br>`return` None
        """
        cls.add(".")
        cls.commit(message)
        cls.push(path, upstream=True)



