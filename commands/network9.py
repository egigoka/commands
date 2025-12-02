#! python3
# -*- coding: utf-8 -*-
"""Internal module with functions to work with network
"""
__version__ = "0.11.0"

import time
from typing import Union


class Network:
    """Class with functions to work with network
    """

    @staticmethod
    def get_domain_of_url(url):
        """
        <br>`param url` string, URL
        <br>`return` string, URL domain
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
    def get_protocol_of_url(url):
        """
        <br>`param url` string, URL
        <br>`return` string, URL domain
        """
        from .str9 import Str
        proto_prefix = "://"
        return Str.substring(url, "", proto_prefix, exception_message="The protocol of url not found") + proto_prefix

    @staticmethod
    def get_ip(domain):
        """Resolve IP from domain name with socket.gethostbyname
        <br>`param domain` string, domain name
        <br>`return` string, IP
        """
        import socket
        try:
            return socket.gethostbyname(domain)  # I don't how it work todo check code of 'socket'
        except socket.gaierror:
            return "not found"

    @classmethod
    def ping(cls,
             domain="127.0.0.1", count=1, quiet=False, timeout=10000):
        """Wrapper under default ping command
        <br>`param domain` string, domain or IP
        <br>`param count` int, count of attempts
        <br>`param quiet` boolean, suppress print to console
        <br>`param timeout` int, timeout in milliseconds
        <br>`param return_ip` boolean, return string with IP
        <br>`return` boolean of availability of domain, or list of boolean domain availability, string ip and full output
                 from ping command
        """
        # todo properly work with exception
        from ping3 import ping
        domain = cls.get_domain_of_url(domain)
        up_message = domain + " is up!"
        down_message = domain + " is down."
        result = None
        if not quiet:
            from .print9 import Print
            Print.rewrite("Pinging", domain, count, "times...")
        try:

            uplink = True
            for i in range(count):

                if i > 0:
                    time.sleep(1)

                result = ping(domain, timeout=int(timeout/1000))

                if type(result) != float:
                    uplink = False
                    break

        except KeyboardInterrupt:
            import sys
            sys.exit()
        except Exception:  # pylint: disable=bare-except
            uplink = False

        if not quiet:
            Print.rewrite("")
            if uplink:
                Print.colored(up_message, "white", "on_green")
            else:
                Print.colored(down_message, "white", "on_red")
        if count == 1:
            return result
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
    def get_global_ip(fast=True, quiet=True):
        # much code by phoemur@gmail.com (ipgetter)
        global Print
        import re
        import random
        import ssl

        from sys import version_info

        import urllib.request as urllib
        import http.cookiejar as cjar

        __version__ = "0.9"

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
                    url = opener.open(server, timeout=1)
                    content = url.read()

                    try:
                        content = content.decode('UTF-8')
                    except UnicodeDecodeError:
                        content = content.decode('ISO-8859-1')

                    m = re.search(
                        r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)',
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

    @staticmethod
    def check_response(endpoint: str, good_response: Union[str, bytes, list, tuple], timeout: int = 10,
                       debug: bool = False) -> bool:
        import requests
        from .list9 import List

        if isinstance(good_response, str):
            good_response = bytes(good_response, encoding="utf-8")
        elif isinstance(good_response, list) or isinstance(good_response, tuple):
            good_response = List.apply_lambda_to_all_elements(good_response, bytes)

        try:
            response = requests.get(endpoint, timeout=timeout).content
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
            if debug:
                from .print9 import Print
                Print.debug(e)
            return False
        if isinstance(good_response, bytes):
            output = response == good_response
        elif isinstance(good_response, list) or isinstance(good_response, tuple):
            output = response in good_response
        else:
            raise TypeError(f"good_response must be bytes, list or tuple, got '{type(good_response)}' instead")
        if debug and not output:
            from .print9 import Print
            Print.debug(response, good_response)
        return output

    @classmethod
    def check_internet_apple(cls, timeout=10, debug=False):
        return cls.check_response("http://captive.apple.com/hotspot-detect.html",
                                  (b'<HTML><HEAD><TITLE>Success</TITLE></HEAD><BODY>Success</BODY></HTML>\n',
                                   b'<HTML><HEAD><TITLE>Success</TITLE></HEAD><BODY>Success</BODY></HTML>'),
                                  timeout=timeout, debug=debug)

    @classmethod
    def check_internet_microsoft(cls, timeout=10, debug=False):
        return cls.check_response("http://www.msftncsi.com/ncsi.txt",
                                  b'Microsoft NCSI',
                                  timeout=timeout, debug=debug)

    @classmethod
    def check_internet_microsoft_connect(cls, timeout=10, debug=False):
        return cls.check_response("http://www.msftconnecttest.com/connecttest.txt",
                                  b'Microsoft Connect Test',
                                  timeout=timeout, debug=debug)

    @classmethod
    def check_internet_google(cls, timeout=10, debug=False):
        import requests
        try:
            response = requests.get("http://connectivitycheck.gstatic.com/generate_204", timeout=timeout)
            output = response.status_code == 204 and response.content == b''
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
            if debug:
                from .print9 import Print
                Print.debug(e)
            return False
        if debug and not output:
            from .print9 import Print
            Print.debug(f"Status: {response.status_code}, Content: {response.content}")
        return output

    @classmethod
    def check_internet_firefox(cls, timeout=10, debug=False):
        return cls.check_response("http://detectportal.firefox.com/success.txt",
                                  b'success\n',
                                  timeout=timeout, debug=debug)

    @staticmethod
    def request(url, method, params=None, basic_auth_user=None, basic_auth_password=None, data=None, json=None,
                headers=None, **kwargs):
        import requests

        auth = None
        if basic_auth_user and basic_auth_password:
            import requests.auth
            auth = requests.auth.HTTPBasicAuth(basic_auth_user, basic_auth_password)

        if method == "get":
            func = requests.get
            kwargs.update({"url": url,
                           "auth": auth,
                           "params": params,
                           "headers": headers})
        elif method == "post":
            func = requests.post
            kwargs.update({"url": url,
                           "auth": auth,
                           "params": params,
                           "data": data,
                           "json": json,
                           "headers": headers})
        elif method == "delete":
            func = requests.delete
            kwargs.update({"url": url,
                           "auth": auth,
                           "params": params,
                           "data": data,
                           "json": json,
                           "headers": headers})
        else:
            raise NotImplementedError(f"Method {method} isn't supported")

        return func(**kwargs)

    @classmethod
    def get(cls, url, params=None, basic_auth_user=None, basic_auth_password=None, headers=None, **kwargs):
        return cls.request(url=url, method="get", params=params, basic_auth_user=basic_auth_user,
                           basic_auth_password=basic_auth_password, headers=headers, **kwargs)

    @classmethod
    def post(cls, url, params=None, data=None, json=None, basic_auth_user=None, basic_auth_password=None, headers=None, **kwargs):
        return cls.request(url=url, method="post", params=params, basic_auth_user=basic_auth_user,
                           basic_auth_password=basic_auth_password, data=data, json=json, headers=headers, **kwargs)

    @classmethod
    def delete(cls, url, params=None, basic_auth_user=None, basic_auth_password=None, headers=None, **kwargs):
        return cls.request(url=url, method="delete", params=params, basic_auth_user=basic_auth_user,
                           basic_auth_password=basic_auth_password, headers=headers, **kwargs)
