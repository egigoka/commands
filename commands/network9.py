#! python3
# -*- coding: utf-8 -*-
"""Internal module with functions to work with network
"""
__version__ = "0.5.3"


class Network:
    """Class with functions to work with network
    """
    @staticmethod
    def get_domain_of_url(url):
        """
        `param url` string, URL
        `return` string, URL domain
        """
        from .str9 import Str
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
        `param domain` string, domain name
        `return` string, IP
        """
        import socket
        try:
            return socket.gethostbyname(domain)  # I don't how it work todo check code of 'socket'
        except socket.gaierror:
            return "not found"

    @classmethod
    def ping(cls,
             domain="127.0.0.1", count=1, quiet=False, logfile=None, timeout=10000, return_ip=False):
        """Wrapper under default ping command
        `param domain` string, domain or IP
        `param count` int, count of attempts
        `param quiet` boolean, suppress print to console
        `param logfile` string, path to log file
        `param timeout` int, timeout in milliseconds
        `param return_ip` boolean, return string with IP
        `return` boolean of availability of domain, or list of boolean domain availability, string ip and full output
                 from ping command
        """
        # todo properly work with exception
        from .os9 import OS
        from .console9 import Console
        domain = cls.get_domain_of_url(domain)
        backup_ping_output = ""
        if not quiet:
            from .print9 import Print
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
        uplink = ping_output.lower().count("ttl") >= count

        if logfile or (not quiet):
            import termcolor
        if logfile:
            raise NotImplementedError()
        #    from .log9 import plog
        #    if uplink:
        #        plog(logfile, domain + " is up!", quiet=True)
        #        termcolor.cprint(up_message, "white", "on_green")
        #    else:
        #        plog(logfile, down_message, quiet=True)
        #        termcolor.cprint(down_message, "white", "on_red")

        elif not quiet:
            Print.rewrite("")
            if uplink:
                termcolor.cprint(up_message, "white", "on_green")
            else:
                termcolor.cprint(down_message, "white", "on_red")
        ip = None  # pylint: disable=invalid-name
        if return_ip:
            from .str9 import Str
            try:
                for line in Str.nl(ping_output + backup_ping_output):
                    if len(Str.get_integers(line, float_support=False)) >= 4:
                        octaves = Str.get_integers(line, float_support=False)  # todo change to regex!!!!!!!!!
                        # pylint: disable=invalid-name
                        ip = str(octaves[0]) + "." + str(octaves[1]) + "." + str(octaves[2]) + "." + str(octaves[3])
                        break
            except TypeError:
                pass
            if not ip:
                ip = cls.dns_lookup(domain)  # pylint: disable=invalid-name
            return uplink, ip, ping_output
        return uplink

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
        from .file9 import File
        from .path9 import Path
        if not out:
            out = os.path.split(url)[1]
        import urllib.request
        response = urllib.request.urlopen(url)
        data = response.read()  # a `bytes` object
        File.write(out, data, mode="wb")
        return Path.full(out)

    @staticmethod
    def get_ip(fast=True, quiet=True):
        # much code by phoemur@gmail.com (ipgetter)
        import re
        import random
        import ssl

        from sys import version_info

        PY3K = version_info >= (3, 0)

        if PY3K:
            import urllib.request as urllib
            import http.cookiejar as cjar
        else:
            import urllib2 as urllib
            import cookielib as cjar

        __version__ = "0.7"
        __version__ = "0.8"  # updated by egigoka@gmail.com

        class IPgetter(object):

            '''
            This class is designed to fetch your external IP address from the internet.
            It is used mostly when behind a NAT.
            It picks your IP randomly from a serverlist to minimize request overhead
            on a single server
            '''

            def __init__(self):
                self.server_list = ['http://ip.dnsexit.com',
                                    # 'http://ifconfig.me/ip',
                                    # 'http://ipecho.net/plain',
                                    # 'http://checkip.dyndns.org/plain',
                                    # 'http://websiteipaddress.com/WhatIsMyIp',
                                    'http://getmyipaddress.org/',
                                    'http://www.my-ip-address.net/',
                                    'http://myexternalip.com/raw',
                                    'http://www.canyouseeme.org/',
                                    'http://www.trackip.net/',
                                    'http://icanhazip.com/',
                                    'http://www.iplocation.net/',
                                    'http://www.ipchicken.com/',
                                    'http://whatsmyip.net/',
                                    'http://www.ip-adress.com/',
                                    # 'http://checkmyip.com/',
                                    'http://www.tracemyip.org/',
                                    'http://www.lawrencegoetz.com/programs/ipinfo/',
                                    'http://www.findmyip.co/',
                                    # 'http://ip-lookup.net/',
                                    # 'http://www.mon-ip.com/en/my-ip/',
                                    'http://ipgoat.com/',
                                    'http://www.myipnumber.com/my-ip-address.asp',
                                    # 'http://formyip.com/',
                                    'https://check.torproject.org/',
                                    # 'http://www.displaymyip.com/',
                                    # 'http://www.bobborst.com/tools/whatsmyip/',
                                    'http://www.geoiptool.com/',
                                    'https://www.whatsmydns.net/whats-my-ip-address.html',
                                    'https://www.privateinternetaccess.com/pages/whats-my-ip/',
                                    'http://checkip.dyndns.com/',
                                    'http://www.ip-adress.eu/',
                                    'http://www.infosniper.net/',
                                    'https://wtfismyip.com/text',
                                    # 'http://ipinfo.io/',
                                    'http://httpbin.org/ip',
                                    'https://diagnostic.opendns.com/myip',
                                    'http://checkip.amazonaws.com',
                                    'https://api.ipify.org',
                                    'https://v4.ident.me']

            def get_external_ip(self):
                '''
                This function gets your IP from a random server
                '''

                myip = ''
                for i in range(7):
                    myip = self.fetch(random.choice(self.server_list))
                    if myip != '':
                        return myip
                    else:
                        continue
                return ''

            def fetch(self, server):
                '''
                This function gets your IP from a specific server.
                '''
                url = None
                cj = cjar.CookieJar()
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                opener = urllib.build_opener(urllib.HTTPCookieProcessor(cj), urllib.HTTPSHandler(context=ctx))
                opener.addheaders = [
                    ('User-agent', "Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0"),
                    ('Accept', "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
                    ('Accept-Language', "en-US,en;q=0.5")]

                try:
                    url = opener.open(server, timeout=4)
                    content = url.read()

                    # Didn't want to import chardet. Prefered to stick to stdlib
                    if PY3K:
                        try:
                            content = content.decode('UTF-8')
                        except UnicodeDecodeError:
                            content = content.decode('ISO-8859-1')

                    m = re.search(
                        '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)',
                        content)
                    myip = m.group(0)
                    return myip if len(myip) > 0 else ''
                except Exception:
                    return ''
                finally:
                    if url:
                        url.close()

            def test(self, quiet=True):
                """
                This functions tests the consistency of the servers
                on the list when retrieving your IP.
                All results should be the same.
                """

                resultdict = {}
                for server in self.server_list:
                    resultdict.update(**{server: self.fetch(server)})

                if not quiet:
                    ips = sorted(resultdict.values())
                    ips_set = set(ips)
                    print('\nNumber of servers: {}'.format(len(self.server_list)))
                    print("IP's :")
                    for ip, ocorrencia in zip(ips_set, map(lambda x: ips.count(x), ips_set)):
                        print('{0} = {1} ocurrenc{2}'.format(ip if len(ip) > 0 else 'broken server', ocorrencia,
                                                            'y' if ocorrencia == 1 else 'ies'))
                    print('\n')
                    print(resultdict)
                return resultdict
        # end code by phoemur@gmail.com

        ipgetter = IPgetter()

        if not fast:
            if not quiet:
                from .print9 import Print
                Print.rewrite("Getting IP...")
            from .dict9 import Dict
            tempdict = {}
            for server, ip in Dict.iterable(ipgetter.test()):
                try:
                    tempdict[ip] += 1
                except KeyError:
                    tempdict[ip] = 1

            most_frequent_ip = 0
            most_frequent_ip_cnt = 0
            for ip, cnt in Dict.iterable(tempdict):
                if cnt > most_frequent_ip_cnt:
                    most_frequent_ip = ip

            if not quiet:
                Print.rewrite()

            if most_frequent_ip:  # do not return empty ip
                return most_frequent_ip
            else:
                raise LookupError("IP not found")
        else:
            return ipgetter.get_external_ip()
