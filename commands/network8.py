#! python3
# -*- coding: utf-8 -*-
"""Internal module with functions to work with network
"""
__version__ = "0.5.0"


class Network:
    """Class with functions to work with network
    """
    @staticmethod
    def get_domain_of_url(url):
        """
        :param url: string, URL
        :return: string, URL domain
        """
        from .str8 import Str
        if "/" in url:
            try:
                url_output = Str.substring(url, "://", "/")
            except KeyError:
                try:
                    url_output = Str.substring(url, "://")
                except KeyError:
                    try:
                        url_output = Str.substring(url, None, "/")
                    except KeyError:
                        url_output = url
        else:
            url_output = url
        return url_output

    @staticmethod
    def dns_lookup(domain):
        """Resolve IP from domain name with socket.gethostbyname
        :param domain: string, domain name
        :return: string, IP
        """
        import socket
        try:
            return socket.gethostbyname(domain)  # I don't how it work todo check code of 'socket'
        except socket.gaierror:
            return "not found"

    @classmethod
    def ping(cls,  # pylint: disable=too-many-arguments,too-many-locals,too-many-branches,too-many-statements
             domain="127.0.0.1", count=1, quiet=False, logfile=None, timeout=10000, return_ip=False):
        """Wrapper under default ping command
        :param domain: string, domain or IP
        :param count: int, count of attempts
        :param quiet: boolean, suppress print to console
        :param logfile: string, path to log file
        :param timeout: int, timeout in milliseconds
        :param return_ip: boolean, return string with IP
        :return: boolean of availability of domain, or list of boolean domain availability, string ip and full output
                 from ping command
        """
        # todo properly work with exception
        from .os8 import OS
        from .console8 import Console
        domain = cls.get_domain_of_url(domain)
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
        except:  # pylint: disable=bare-except
            #  any exception is not good ping
            try:
                backup_ping_output = ping_output
            except UnboundLocalError:
                backup_ping_output = ""
            ping_output = ""
        up = ("TTL" in ping_output) or ("ttl" in ping_output)  # pylint: disable=invalid-name

        if logfile or (not quiet):
            import termcolor
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
        ip = None  # pylint: disable=invalid-name
        if return_ip:
            from .str8 import Str
            try:
                for line in Str.nl(ping_output + backup_ping_output):
                    if len(Str.get_integers(line, float_support=False)) >= 4:
                        octaves = Str.get_integers(line, float_support=False)
                        # pylint: disable=invalid-name
                        ip = str(octaves[0]) + "." + str(octaves[1]) + "." + str(octaves[2]) + "." + str(octaves[3])
                        break
            except TypeError:
                pass
            if not ip:
                ip = cls.dns_lookup(domain)  # pylint: disable=invalid-name
            return up, ip, ping_output
        return up

    @staticmethod
    def get_fqdn(ip=None):
        import socket
        if ip:
            return socket.getfqdn(ip)
        return socket.getfqdn()

    @staticmethod
    def get_netbios(ip):
        import socket
        if ip:
            socket.gethostbyaddr(ip)
        return socket.gethostname()

    @staticmethod
    def download_file(url, out=None, quiet=None):
        import os
        from .file8 import File
        from .path8 import Path
        if not out:
            out = os.path.split(url)[1]
        import urllib.request
        response = urllib.request.urlopen(url)
        data = response.read()  # a `bytes` object
        File.write(out, data, mode="wb")
        return Path.full(out)

    @staticmethod
    def get_ip(extended=False):
        try:
            import ipgetter
        except ImportError:
            from .pip8 import Pip
            Pip.install("ipgetter")
            import ipgetter

        if extended:
            return ipgetter.IPgetter().test()
        else:
            return ipgetter.myip()
