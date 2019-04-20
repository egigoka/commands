import re
from commands import *

regexp = r'\"\"\".*?\"\"\"'

files = Dir.list_of_files(Path.combine(Path.working(), "commands"))

for file in files:
    filepath = Path.combine(Path.working(), "commands", file)
    filecontent = File.read(filepath)
    for docstring in re.findall(regexp, filecontent, re.S):
        print()
        print(docstring)
        new_docstring = docstring.replace(" `", " <br>`")
        filecontent = filecontent.replace(docstring, new_docstring)
        File.wipe(filepath)
        File.write(filepath, filecontent)