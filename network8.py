#! python3
# -*- coding: utf-8 -*-
__version__ = "0.0.2"


class Network:
    @staticmethod
    def get_domain_of_url(url):
        from .str8 import Str
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
    def ping(Network, domain="127.0.0.1", count=1, quiet=False, logfile=None, timeout=10000, return_ip=False):
        # todo properly work with exception
        from .os8 import OS
        from .console8 import Console
        domain = Network.get_domain_of_url(domain)
        backup_ping_output = ""
        if not quiet:
            from .print8 import Print
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
                timeout = int(timeout / 1000)
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
            from .log8 import plog
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
                for line in Str.nl(ping_output + backup_ping_output):
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