import os
from commands import *

command = "pylint "
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith(".py"):
            command += fr"{Path.combine(root, file).lstrip('.').lstrip(backslash)} "
command += fr"--max-line-length=120"
                    
Process.start(command, pureshell=True)
