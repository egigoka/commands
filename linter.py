import os
from commands import Process, Path, backslash

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith(".py"):
            Process.start(" ".join(["pylint", Path.combine(root, file).lstrip('.').lstrip(backslash),
                                    "--max-line-length=120"]), pureshell=True)
