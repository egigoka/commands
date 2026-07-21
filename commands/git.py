#! python3
# -*- coding: utf-8 -*-
"""Internal module to simplify work with git."""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import os
    from typing import Optional
    from .bash import Bash
    from .console import Console
    from .path import Path

from .module import LazyModule, LazyProperty
# pylint: disable=unused-wildcard-import, wildcard-import

__version__ = "2.2.0"
if not TYPE_CHECKING:
    os = LazyModule("os")
    Path = LazyProperty(".path", "Path")
    Console = LazyProperty(".console", "Console")
    Bash = LazyProperty(".bash", "Bash")


def get_name_of_repo() -> str:
    """Return the repo name for the current working directory.

    <br>`return` string, name of repo
    """
    if Path.working().split(os.sep)[-1] in ["t", "term"]:
        return "test"
    return Path.working().split(os.sep)[-1]


class Git:
    """Class to simplify work with git, wrapper for cli git."""

    def __init__(self, remote: Optional[str] = None) -> None:
        self.remote = remote
        self._commit_message: Optional[str] = None

    def __call__(
        self,
        message: Optional[str] = None,
        remote: Optional[str] = None,
        add: bool = True,
        push: bool = True,
        verbose: bool = False
    ) -> bool:
        """Run add/commit/push with stored or provided defaults in one go."""
        if remote:
            self.remote = remote
        if message:
            self._commit_message = message
        if not self._commit_message:
            raise ValueError("Commit message must be set")
        if add:
            self.add_files(verbose=verbose)
        self.commit_changes(message=self._commit_message, verbose=verbose)
        if push:
            self.push_remote(upstream=True, verbose=verbose)
        return True

    @classmethod
    def add(cls, what: str, verbose: bool = False) -> None:
        """Add files to the next commit.

        <br>`param what` string, adding files
        <br>`return` None
        """
        Console.get_output("git", "add", what, print_std=verbose)

    @classmethod
    def commit(cls, message: Optional[str] = None, verbose: bool = False) -> None:
        """Commit all added changes.

        <br>`param message` string, message of commit
        <br>`return` None
        """
        commands = ["git", "commit"]
        if message:
            commands.append("-m")
            commands.append(Bash(message).escape())
        Console.get_output(commands, print_std=verbose)

    @classmethod
    def push(cls, path: str, upstream: bool = False, verbose: bool = False) -> None:
        """Push commits to a repo.

        <br>`param path` string, path of repo
        <br>`param upstream` boolean, if True, adding argument '-u' to git
        <br>`return` None
        """
        commands = ["git", "push"]
        if upstream:
            commands.append("-u")
        commands.append(path)
        Console.get_output(commands, print_std=verbose)

    @classmethod
    def update(cls, message: str, path: str = "https://github.com/egigoka/" + get_name_of_repo() + ".git", verbose: bool = False) -> None:
        """Automate adding, committing, and pushing changes.

        <br>`param message` string, commit message
        <br>`param path` string, path to repo
        <br>`return` None
        """
        cls.add(".", verbose=verbose)
        cls.commit(message, verbose=verbose)
        cls.push(path, upstream=True, verbose=verbose)

    # Instance-friendly helpers
    def add_files(self, what: str = ".", verbose: bool = False) -> None:
        """Instance wrapper for add."""
        return self.__class__.add(what, verbose=verbose)

    def commit_changes(self, message: Optional[str] = None, verbose: bool = False) -> None:
        """Instance wrapper for commit."""
        return self.__class__.commit(message=message, verbose=verbose)

    def push_remote(self, upstream: bool = False, verbose: bool = False) -> None:
        """Push to the configured remote."""
        if not self.remote:
            raise ValueError("Remote path is not set")
        return self.__class__.push(self.remote, upstream=upstream, verbose=verbose)

    def update_remote(self, message: str, verbose: bool = False) -> None:
        """Update the configured remote with a commit."""
        remote = self.remote or "https://github.com/egigoka/" + get_name_of_repo() + ".git"
        return self.__class__.update(message=message, path=remote, verbose=verbose)
