#! python3
# -*- coding: utf-8 -*-
"""Internal module to create counters
"""
__version__ = "0.0.1"

class ID:
    def __init__(self):
        self.cnt = -1

    def get(self):
        self.cnt += 1
        return self.cnt