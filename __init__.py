#! python3
# -*- coding: utf-8 -*-
import datetime
start_bench_no_bench = datetime.datetime.now()
__version__ = "9.0.0-prealpha"
# TODO for 9.0.0 release:
    # !done! OS class vars not strings, but booleans
    # !done! lazy load for all modules
    # !done! all submodules lazy load
    # fix Time.rustime without cyrillic_support
    # Console.get_output make ouptut even if exit status != 0
    # make tests for all
    # PIP8 check for all
    # docstrings for all
    # new dir_c
# TODO version diff
#   todo export script as json?
#   todo compare jsons?
#   todo save changes as commit message?

FRACKING_classes_speed_tweaking = False
FRACKING_classes_speed_tweaking = True




try:

    bench_no_bench_import_time = datetime.datetime.now()

    from .bench8 import get_Bench

    if FRACKING_classes_speed_tweaking:
        LoadTimeBenchMark = get_Bench()
        LoadTimeBenchMark.fraction_digits = 4
        LoadTimeBenchMark.time_start = start_bench_no_bench
        LoadTimeBenchMark.end("init in", quiet_if_zero=True)
        LoadTimeBenchMark.time_start = bench_no_bench_import_time
        LoadTimeBenchMark.end("func get_Bench loaded in", quiet_if_zero=True, start_immideately=True)

    from .str8 import Str

    if FRACKING_classes_speed_tweaking:
        LoadTimeBenchMark.end("class Str loaded in", quiet_if_zero=True, start_immideately=True)  # python searching for that module in PATH

    from .os8 import OS

    if FRACKING_classes_speed_tweaking:
        LoadTimeBenchMark.end("class OS loaded in", quiet_if_zero=True, start_immideately=True)

    from .print8 import Print

    if FRACKING_classes_speed_tweaking:
        LoadTimeBenchMark.end("class Print loaded in", quiet_if_zero=True, start_immideately=True)

    class Internal:
        @staticmethod
        def dir_c():
            """Print all functionality of commands8
            """
            raise NotImplementedError
            # commands.__dict__



        @staticmethod
        def rel(quiet=False):  # d reload commands8, if you use it not in REPL, activate quiet argument
          # d require additional line of code after reload if you import not entrie commands8
          # d you need manually add "from commands8 import *" to script/REPL
          # d if you import like "import commands8", additional line of code not needed
            import commands, importlib
            commands = importlib.reload(commands8)
            del commands
            string = "from commands import *"  # d you need to manually add this <<< string to code :(
            if not quiet:
                print('"'+string+'" copied to clipboard')
                import copypaste
                copypaste.copy(string)
                pass

    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Internal loaded in", quiet_if_zero=True, start_immideately=True)

    from .const8 import *

    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("imported constants in", quiet_if_zero=True, start_immideately=True)

    from .console8 import Console

    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Console loaded in", quiet_if_zero=True, start_immideately=True)

    class Ssh:
        @staticmethod
        def get_output(host, username, password, command, safe=False):  # return
          # d output from command, runned on SSH server. Support only
          # d username:password autorisation.
          # todo autorisation by key.
            if OS.python_implementation != "pypy":
                import paramiko
            else:
                raise OSError("paramiko doesn't supported by PyPy")
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # automatically add unknown hosts
            ssh.connect(host, username=username, password=password)
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("uptime")
            if (ssh_stderr.read() != b'') and not safe:
                raise IOError("ssh_stderr = " + str(ssh_stderr))
            ssh.close()
            return str(ssh_stdout.read(), 'utf8')

        @classmethod
        def get_avg_load_lin(cls, host, username, password, safe=False):  # return
          # d list of average loads from SSH linux server. Shit, I know
            output = cls.get_output(host=host, username=username, password=password, command="uprime", safe=safe)
            output = Str.substring(output, before="load average: ", after=newline)
            output = output.split(", ")
            return output

        @classmethod
        def get_uptime_lin(cls, host, username, password, safe=False):  # return
          # d string with uptime of SSH linux server. As I said before... :(
            output = cls.get_output(host=host, username=username, password=password, command="uprime", safe=safe)
            output = Str.substring(output, before=" up ", after=", ")
            return output


    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Ssh loaded in", quiet_if_zero=True, start_immideately=True)


    class Path:
        @staticmethod
        def full(path):
            import os
            return os.path.abspath(path)

        @staticmethod
        def commands8():
            import os
            return os.path.dirname(os.path.realpath(__file__))

        @staticmethod
        def working():
            import os
            return os.getcwd()

        @classmethod
        def extend(cls, *paths, debug=False):  # paths input strings of path pieces, return
          # d string with path, good for OS
            import os
            for path_part in paths:
                try:
                    path = os.path.join(str(path), str(path_part))
                except NameError:  # first path piece is very important
                    if (OS.windows) and path_part == backslash:  # support for smb windows paths like \\ip_or_pc\dir\
                        path = backslash * 2
                    elif (OS.windows) and (len(path_part) <= 3):
                        path = os.path.join(path_part, os.sep)
                    elif OS.windows:
                        path = path_part
                        if debug: Print.debug("path", path, "path_part", path_part)
                    elif OS.unix_family:
                        if path_part == "..":
                            path = path_part
                        elif path_part == ".":
                            path = path_part
                        elif path_part == "~":
                            path = cls.home()
                        else:
                            path = os.path.join(os.sep, path_part)
                    else:
                        raise FileNotFoundError("path_part" + str(path_part) + "is not expected")

            return path

        @staticmethod
        def home():  # return path of home directory of current user. Not tested in
          # d linux.
          # todo test in lunux!
            if OS.windows:
                path = Console.get_output(r"echo %userprofile%")
                path = path.rstrip(newline2)
            else:
                path = Console.get_output("echo $HOME", split_lines=True)[0]
                path = path.rstrip(newline)
            return path

        @staticmethod
        def set_current(path, quiet=True):
            """changes current working directory. If quiet is disabled, prints
            directory.
            """
            import os
            os.chdir(path)
            if not quiet:
                Print.debug("os.getcwd()  # current directory is", os.getcwd())


    class Locations:
        if OS.windows:  # d ...
            texteditor = "notepad"  # d notepad is in every version of Windows, yea?
            py = "py"
            pyw = "pyw"
        elif OS.macos:  # d ...
            texteditor = "open"  # d just open default program for file
            py = "python3"
            pyw = "python3"
        elif OS.linux:  # d ...
            texteditor = "nano"  # d nano is everywhere, I suppose? ]-:
            py = "python3"
            pyw = "python3"

    class Dir:
        @staticmethod
        def create(filename):  # create dir if didn't exist
            import os
            if not os.path.exists(filename):
                os.makedirs(filename)

        @staticmethod
        def commands8(): return Path.commands8()  # alias to Path.commands8

        @staticmethod
        def working(): return Path.working()  # alias to Path.working

        @staticmethod
        def list_of_files(path):  # return list of files in folder
            import os
            return os.listdir(path)

        @staticmethod
        def number_of_files(path, quiet=False):
            """Return integer of number of files in directory
            """
            import os
            try:
                dir_contents = Dir.contents(path)
                if not quiet:
                    print(os.path.split(path)[1], "contain", len(dir_contents), "files")
                return len(dir_contents)
            except FileNotFoundError:
                if not quiet:
                    print("Path", path, "isn't found")
                return None

        @classmethod
        def batch_rename(cls, directory, input_str, output_str, quiet=False):
            for filename in cls.contain(directory):
                if input_str in filename:
                    final_name = filename.replace(input_str, output_str)
                    File.rename(filename, final_name)
                    if not quiet:
                        print(filename, "renamed to", final_name)

    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Path loaded in", quiet_if_zero=True, start_immideately=True)

    class File:
        @staticmethod
        def create(filename):
            import os
            filename = Path.full(filename)
            if os.path.split(filename)[0] != "":
                Dir.create(os.path.split(filename)[0])
            if not File.exists(filename):
                with open(filename, 'a'):  # open file and close after
                    os.utime(filename, None)  # change time of file modification
            else:
                raise FileExistsError("file" + str(filename) + "exists")
            if not File.exists(filename):
                import sys
                raise FileNotFoundError("error while creating file " + filename +
                                        "try to repair script at " + Path.full(sys.argv[0]))

        @staticmethod
        def delete(path, quiet=False):  # ...
            import time, os
            if os.path.isdir(path):
                raise IsADirectoryError(path + " is directory, use Dir.delete to delete")
            try:
                os.remove(path)
            except FileNotFoundError:
                if not quiet:
                    print("file", path, "is not exist")
            if not quiet:
                print("file", path, "is deleted")
            time.sleep(0.05)
            if File.exists(path):
                raise FileExistsError(path + " is not deleted")

        @staticmethod
        def move(input_file, output_file):  # ...
            import shutil
            shutil.move(input_file, output_file)

        @staticmethod
        def copy(input_file, output_file):  # ...
            import shutil
            shutil.copy2(input_file, output_file)

        @staticmethod
        def rename(input_file, output_file):  # ...
            File.move(input_file, output_file)

        @staticmethod
        def hide(filename, quiet=True):
            """adding dot to filename and set attribute FILE_ATTRIBUTE_HIDDEN to
            file, if running on Windows"""
            import os
            filename = Path.full(filename)
            if OS.windows:
                import win32api, win32con
                win32api.SetFileAttributes(filename, win32con.FILE_ATTRIBUTE_HIDDEN)  # hiding file like windows do
            dotted_file = Path.extend(os.path.split(filename)[0], "." + os.path.split(filename)[1])  # adding dot
            File.rename(filename, dotted_file)
            if not quiet:
                print ("file", filename, "is hidden now")
            return dotted_file

        @classmethod
        def backup(cls, filename, subfolder="bak", hide=True, quiet = False):
            """Move file to subfolder, adds sort of timestamp to filename and
            hide file if same named argument is True
            """
            import os
            import shutil
            filename = Path.full(filename) # normalize filename
            backupfilename = str(filename) + "." + Time.dotted() + ".bak"  # add dottedtime to backup filename
            backupfilename = os.path.split(backupfilename)  # splitting filename to folder and file
            try:  # if subfolder has no len
                if len(subfolder) < 1:  # if subfolder has zero len
                    raise TypeError("subfolder must have non-zero len")
            except TypeError:  # if subfolder has no len
                subfolder = "bak"  # set subfolder to default
                print("len(subfolder) < 1, so subfolder = 'bak'")  # print error
            subfolder = Path.extend(backupfilename[0], subfolder)  # append subfolder name
            Dir.create(subfolder)  # create subfolder
            backupfilename = Path.extend(subfolder, backupfilename[1])  # backup file name full path
            shutil.copy2(filename, backupfilename)  # finally backup file
            if hide:
                backupfilename = cls.hide(backupfilename)  # hiding file
            if not os.path.isfile(backupfilename):  # if file is not created
                raise FileNotFoundError(backupfilename + " isn't created while backup")
            if not quiet:  # if finction is not shutted up
                print("backup of file", filename, "created as", backupfilename) # all is ok, print that
            return backupfilename

        @staticmethod
        def wipe(path):  # clean content of file
            file = open(path, 'w')
            file.close()

        @staticmethod
        def read(path):  # return pipe to file content
            with open(path, "r", encoding='utf-8') as f:
                return f.read()

        @staticmethod
        def write(filename, what_to_write, mode="ab"):
            """write to end of file with default mode, you can change it to any
            that supported by python open() func"""
            with open(filename, mode=mode) as file:  # open file then closes it
                file.write(what_to_write.encode("utf-8"))

        @staticmethod
        def get_size(filename):  # return size in bytes
            import os
            return os.stat(filename).st_size

        @staticmethod
        def exists(filename):
            import os
            return os.path.exists(filename)

    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class File loaded in", quiet_if_zero=True, start_immideately=True)

    from .time8 import Time

    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Time loaded in", quiet_if_zero=True, start_immideately=True)

    class Json():
        @classmethod
        def check(cls, filename):
            try:
                cls.load(filename)
                return True
            except:  # any exception is False
                print("JSON is bad")
                return False

        @classmethod
        def save(cls, filename, jsonstring, quiet=False, debug=False):
            import json, sys
            try:
                File.wipe(filename)
                settingsJsonTextIO = open(filename, "w")
                json.dump(jsonstring, settingsJsonTextIO)
                settingsJsonTextIO.close()
                if not quiet:
                    print("JSON succesfull saved")
                if debug:
                    print("sys.argv[0] =",sys.argv[0])
                    print(jsonstring)
            except:
                raise IOError("error while saving JSON, try to repair script at path " +
                              Path.full(sys.argv[0]))
            json_test_string = cls.load(filename, quiet=True)
            if jsonstring != json_test_string:
                Print.debug("jsonstring_to_save", jsonstring, "json_test_string_from_file", json_test_string)
                raise IOError("error while saving JSON, try to repair script at path " +
                              Path.full(sys.argv[0]))  # exception

        @classmethod
        def load(cls, filename, quiet = False, debug=False):
            import json, os
            try:
                if not os.path.isfile(filename):
                    File.create(filename)
                    cleanjson = {}
                    cls.save(filename, cleanjson)
                settingsJsonTextIO = open(filename)
                jsonStringInMemory = json.load(settingsJsonTextIO)
                settingsJsonTextIO.close()
                if not quiet:
                    print("JSON succesfull loaded")
                if debug:
                    print(jsonStringInMemory)
                return jsonStringInMemory
            except:
                import sys
                raise IOError("error while loading JSON, try to repair script at path " +
                              Path.full(sys.argv[0]))

    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Json loaded in", quiet_if_zero=True, start_immideately=True)

    from .list8 import List

    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class List loaded in", quiet_if_zero=True, start_immideately=True)

    from .process8 import Process

    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Process loaded in", quiet_if_zero=True, start_immideately=True)

    class Dict:
        @staticmethod
        def iterable(dict_):
            if not isinstance(dict_, dict):
                raise TypeError("There must be dict in input")
            return dict_.items()

        @staticmethod
        def sorted_by_key(dict, case_insensitive=False):
            if case_insensitive == True:
                output = {}
                for i in sorted(dict, key=str.lower):
                    output[i] = dict[i]
                return output
            else:
                import collections
                return collections.OrderedDict(sorted(dict.items()))

    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Dict loaded in", quiet_if_zero=True, start_immideately=True)

    class Codegen:
        debug = False

        @classmethod
        def start(cls, file_path):
            File.wipe(file_path)
            cls.file = open(file_path, "wb")

        @classmethod
        def add_line(cls, code):
            cls.file.write(code.encode('utf8'))
            if cls.debug:
                print(code)

        @classmethod
        def end(cls, quiet=False):
            cls.file.close()

        shebang = "#! python3" + newline + \
                  "# -*- coding: utf-8 -*-" + newline

    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Codegen loaded in", quiet_if_zero=True, start_immideately=True)

    def plog(logfile, logstring="some shit happened", customtime=None, quiet=False, backup=True):
        if not quiet:
            print(logstring)
        File.create(logfile)
        if backup:
            File.backup(logfile, quiet=True)
        file = open(logfile, "a")
        if customtime:
            file.write(Time.rustime(customtime) + " " + str(logstring) + newline)
        else:
            file.write(Time.rustime() + " " + str(logstring) + newline)
        file.close()

    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("func plog loaded in", quiet_if_zero=True, start_immideately=True)

    class Network:
        @staticmethod
        def getDomainOfUrl(url):
            url_output = Str.substring(url, "://", "/")
            if url_output == "":
                url_output = Str.substring(url, "://")
            return url_output

        @staticmethod
        def dnslookup(domain):
            import socket
            try:
                return socket.gethostbyname(domain)  # I don't how it work todo check code of 'socket'
            except socket.gaierror:
                return "not found"

        @classmethod
        def ping(Network, domain ="127.0.0.1", count=1, quiet=False, logfile=None, timeout=10000, return_ip=False):
            # с таким эксепшном можно сделать куда проще это всё
            domain = Network.getDomainOfUrl(domain)
            backup_ping_output = ""
            if not quiet:
                Print.rewrite("Pinging", domain, count, "times...")
                up_message = domain + " is up!"
                down_message = domain + " is down."
            try:
                if OS.windows:
                    count_arg = "n"
                    timeout_arg = "w"
                if OS.unix_family:
                    count_arg = "c"
                    timeout_arg = "W"
                if OS.linux:
                    timeout = int(timeout/1000)
                command = "ping " + domain + " -" + count_arg + " " + str(count) + \
                          " -" + timeout_arg + " " + str(timeout)
                ping_output = Console.get_output(command)

            except KeyboardInterrupt:
                import sys
                sys.exit()
            except:  # any exception is not good ping
                try:
                    backup_ping_output = ping_output
                except UnboundLocalError:
                    backup_ping_output = ""
                ping_output = ""
            if ("TTL" in ping_output) or ("ttl" in ping_output):
                up = True
            else:
                up = False

            if logfile or (not quiet): import termcolor
            if logfile:
                if up:
                    plog(logfile, domain + " is up!", quiet=True)
                    termcolor.cprint(up_message, "white", "on_green")
                else:
                    plog(logfile, down_message, quiet=True)
                    termcolor.cprint(down_message, "white", "on_red")

            elif not quiet:
                Print.rewrite("")
                if up:
                    termcolor.cprint(up_message, "white", "on_green")
                else:
                    termcolor.cprint(down_message, "white", "on_red")
            ip = None
            if return_ip:
                try:
                    for line in Str.nl(ping_output+backup_ping_output):
                        if len(Str.get_integers(line)) >= 4:
                            octaves = Str.get_integers(line)
                            ip = str(octaves[0]) + "." + str(octaves[1]) + "." + str(octaves[2]) + "." + str(octaves[3])
                            break
                except TypeError:
                    pass
                if not ip:
                    ip = Network.dnslookup(domain)
                return up, ip, ping_output
            return up

    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Network loaded in", quiet_if_zero=True, start_immideately=True)

    class Fix:

        def winRepair_UnicodeEncodeError(quiet=""):
            import os
            if quiet:
                quiet = " > null"
            os.system("chcp 65001" + quiet)
            os.system("set PYTHONIOENCODING = utf - 8")


    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Fix loaded in", quiet_if_zero=True, start_immideately=True)

    class Bash:
        escapable_chars = [backslash]
        @classmethod
        def argument_escape(cls, argument):
            for char in cls.escapable_chars:
                argument = argument.replace(char, backslash+char)
            return Str.to_quotes(argument)

    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Bash loaded in", quiet_if_zero=True, start_immideately=True)

    if OS.macos:
        from .macos8 import macOS

    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class macOS loaded in", quiet_if_zero=True, start_immideately=True)

    from .gui8 import Gui

    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Gui loaded in", quiet_if_zero=True, start_immideately=True)

    class Tkinter():
        @staticmethod
        def color(red, green, blue):  # return string of color matching for use in
          # d Tkinter
            return str('#%02x%02x%02x' % (red, green, blue))

    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Tkinter loaded in", quiet_if_zero=True, start_immideately=True)

    if OS.windows:
        class Windows:
            @staticmethod
            def lock():  # locking screen, work only on Windows < 10
                if OS.windows_version and (OS.windows_version != 10):
                    import ctypes
                    ctypes.windll.LockWorkStation()  # todo fix Windows 10
                else:
                    raise OSError("Locking work only on Windows < 10")

    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Windows loaded in", quiet_if_zero=True, start_immideately=True)

    from .random8 import Random

    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Random loaded in", quiet_if_zero=True, start_immideately=True)

    class Wget:
        @staticmethod
        def download(url, output, quiet=False):  # just wrapper for commandline wget
            arguments = '--header="Accept: text/html" ' + \
                        '--user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) ' + \
                        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3167.0 Safari/537.36"'
            if quiet:
                command = "wget '" + url + "' -O " + output + " " + arguments
                return Console.get_output(command)
            else:
                url = url.replace("&", backslash + "&")
                Process.start("wget", url, "-O", output, arguments, pureshell=True)
            # Another way to fix blocks by creating ~/.wgetrc file https://stackoverflow.com/a/34166756

    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Wget loaded in", quiet_if_zero=True, start_immideately=True)

    from .int8 import Int

    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class Int loaded in", quiet_if_zero=True, start_immideately=True)

    from .cli8 import CLI

    if FRACKING_classes_speed_tweaking: LoadTimeBenchMark.end("class CLI loaded in", quiet_if_zero=True, start_immideately=True)

    LoadTimeBenchMark = get_Bench()
    LoadTimeBenchMark.time_start = start_bench_no_bench


    class __build__:
        build_json_file = Path.extend(Path.commands8(), "buildnumber.json")
        try:
            build = Json.load(build_json_file, quiet=True)[0]
        except:
            build = "NaN"
        Json.save(build_json_file, [build+1], quiet=True)


    LoadTimeBenchMark.end("commands8 v" + __version__ + "-'build'-" + str(__build__.build) + " loaded in")
except ModuleNotFoundError:
    import console.installreq8
    from .print8 import Print
    Print.debug("I tried my best to install dependencies, try to restart script, everything must be okay")
