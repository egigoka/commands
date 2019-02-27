import os
from commands import *

for root, dirs, files in os.walk('.'):
    for file in files:
            if file.endswith(".py"):
                    Process.start(fr"pylint {Path.combine(root, file).lstrip('.').lstrip(backslash)} --max-line-length=120{newline}", pureshell=True)
