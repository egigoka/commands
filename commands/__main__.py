#! python3
# -*- coding: utf-8 -*-
"""Stub for load module."""
# pylint: disable=wrong-import-position
from .module import LazyModule

sys = LazyModule("sys")
commands = LazyModule("commands")
sys.path.insert(0, ".")
globals().update(commands.__dict__)
