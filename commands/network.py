#! python3
# -*- coding: utf-8 -*-
"""Internal module with functions to work with network."""
from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import http.cookiejar as cjar
    import os
    import random
    import re
    import socket
    import ssl
    import sys
    import time
    import urllib.request as request
    import urllib.request as urllib
    from typing import Any, Optional, Tuple, Union, cast
else:
    def cast(_type, value):
        """Return value unchanged for runtime typing fallback."""
        return value

from .module import LazyModule, LazyProperty

__version__ = "0.12.0"
if not TYPE_CHECKING:
    socket = LazyModule("socket")
    sys = LazyModule("sys")
    os = LazyModule("os")
    request = LazyModule("urllib.request")
    re = LazyModule("re")
    random = LazyModule("random")
    ssl = LazyModule("ssl")
    urllib = LazyModule("urllib.request")
    cjar = LazyModule("http.cookiejar")
Str = LazyProperty(".str", "Str")
OS = LazyProperty(".os", "OS")
Print = LazyProperty(".print", "Print")
File = LazyProperty(".file", "File")
Path = LazyProperty(".path", "Path")
Dict = LazyProperty(".dict", "Dict")
List = LazyProperty(".list", "List")

if not TYPE_CHECKING:
    time = LazyModule("time")
requests = LazyModule("requests")


class Network:
    """Class with functions to work with network."""

    ping: Any
    get_ip: Any
    get_fqdn: Any

    def __init__(self, target: Optional[str] = None) -> None:
        self.target = target
        self.timeout = 10000
        self.count = 1

    def __call__(
        self,
        target: Optional[str] = None,
        count: Optional[int] = None,
        timeout: Optional[int] = None,
        verbose: bool = False
    ) -> Any:
        """Ping via instance or update target."""
        if target:
            self.target = target
        if self.target is None:
            raise ValueError("Network target is not set")
        if count is not None:
            self.count = count
        if timeout is not None:
            self.timeout = timeout
        return self.ping(count=self.count, verbose=verbose, timeout=self.timeout)

    @property
    def domain(self) -> str:
        """Return the domain derived from the target URL."""
        if self.target is None:
            raise ValueError("Network target is not set")
        return self.get_domain_of_url(self.target)

    def _ping_instance(self, count: int = 1, verbose: bool = False, timeout: int = 10000) -> Any:
        """Instance shortcut for Network.ping using stored target."""
        if self.target is None:
            raise ValueError("Network target is not set")
        return type(self).ping(self.target, count=count, verbose=verbose, timeout=timeout)

    def _get_ip_instance(self) -> str:
        if self.target is None:
            raise ValueError("Network target is not set")
        return str(type(self).get_ip(self.domain))

    def _get_fqdn_instance(self) -> str:
        if self.target is None:
            raise ValueError("Network target is not set")
        return str(type(self).get_fqdn(self.domain))

    @classmethod
    def get_domain_of_url(cls, url: str) -> str:
        """Return the domain part of a URL.

        <br>`param url` string, URL
        <br>`return` string, URL domain
        """
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
        return str(url_output)

    @classmethod
    def get_protocol_of_url(cls, url: str) -> str:
        """Return the protocol part of a URL.

        <br>`param url` string, URL
        <br>`return` string, URL domain
        """
        proto_prefix = "://"
        protocol = Str.substring(url, "", proto_prefix, exception_message="The protocol of url not found")
        return str(protocol) + proto_prefix

    @classmethod
    def _get_ip_class(cls, domain: str) -> str:
        """Resolve IP from a domain name using socket.gethostbyname.

        <br>`param domain` string, domain name
        <br>`return` string, IP
        """
        try:
            return socket.gethostbyname(domain)  # I don't how it work todo check code of 'socket'
        except socket.gaierror:
            return "not found"

    @classmethod
    def _ping_class(cls,
             domain: str = "127.0.0.1", count: int = 1, verbose: bool = False, timeout: int = 10000) -> Any:
        """Run a ping command and return availability.

        <br>`param domain` string, domain or IP
        <br>`param count` int, count of attempts
        <br>`param verbose` boolean, suppress print to console
        <br>`param timeout` int, timeout in milliseconds
        <br>`param return_ip` boolean, return string with IP
        <br>`return` boolean of availability of domain, or list of boolean domain availability, string ip and full output
                 from ping command
        """
        # todo properly work with exception
        domain = cls.get_domain_of_url(domain)
        up_message = domain + " is up!"
        down_message = domain + " is down."
        result = None
        if verbose:
            Print.rewrite("Pinging", domain, str(count), "times...")
        try:

            uplink = True
            for i in range(count):

                if i > 0:
                    time.sleep(1)

                ping_func = getattr(OS, "ping", None)
                if isinstance(ping_func, staticmethod):
                    ping_func = ping_func.__func__
                if ping_func is None:
                    raise OSError("OS ping function is not available")
                result = ping_func(domain, timeout=int(timeout/1000))

                if type(result) != float:
                    uplink = False
                    break

        except KeyboardInterrupt:
            sys.exit()
        except Exception:  # pylint: disable=bare-except
            uplink = False

        if verbose:
            Print.rewrite("")
            if uplink:
                Print.colored(up_message, "white", "on_green")
            else:
                Print.colored(down_message, "white", "on_red")
        if count == 1:
            return result if uplink else False
        return uplink

    @classmethod
    def _get_fqdn_class(cls, ip: Optional[str] = None) -> str:
        if ip:
            return socket.getfqdn(ip)
        return socket.getfqdn()

    @classmethod
    def get_netbios(cls, ip: Optional[str]) -> str:
        """Return the NetBIOS name for an IP."""
        if ip:
            socket.gethostbyaddr(ip)
        return socket.gethostname()

    @classmethod
    def download_file(cls, url: str, out: Optional[str] = None, verbose: Optional[bool] = None) -> str:
        """Download a URL to a local file and return the path."""
        if not out:
            out = os.path.split(url)[1]
        response = urllib.urlopen(url)
        data = response.read()  # a `bytes` object
        File.write(out, data, mode="wb")
        return str(Path.full(out))

    @classmethod
    def get_global_ip(cls, fast: bool = True, verbose: bool = False) -> str:
        """Get the external IP address."""
        # much code by phoemur@gmail.com (ipgetter)


        __version__ = "0.9"

        class _IPgetter(object):
            """Fetch an external IP address from the internet.

            It is used mostly when behind a NAT. It picks your IP randomly from a
            server list to minimize request overhead on a single server.
            """

            def __init__(self) -> None:
                self.server_list: list[str] = ['http://ip.dnsexit.com',
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

            def get_external_ip(self) -> str:
                """Get your IP from a random server."""
                myip = ''
                for i in range(7):
                    myip = self.fetch(random.choice(self.server_list))
                    if myip != '':
                        return myip
                    else:
                        continue
                return ''

            def fetch(self, server: str) -> str:
                """Get your IP from a specific server."""
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
                    if m is None:
                        return ''
                    myip = m.group(0)
                    return myip if len(myip) > 0 else ''
                except Exception:
                    return ''
                finally:
                    if url:
                        url.close()

            def test(self, verbose: bool = False) -> dict[str, str]:
                """Test consistency of servers when retrieving your IP.

                All results should be the same.
                """
                resultdict: dict[str, str] = {}
                for server in self.server_list:
                    resultdict.update(**{server: self.fetch(server)})

                if verbose:
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

        ipgetter_cls = globals().get("IPgetter", _IPgetter)
        ipgetter = ipgetter_cls()

        if not fast:
            if verbose:
                Print.rewrite("Getting IP...")
            tempdict: dict[str, int] = {}
            for server, ip in Dict.iterable(ipgetter.test(verbose=verbose)):
                try:
                    tempdict[ip] += 1
                except KeyError:
                    tempdict[ip] = 1

            most_frequent_ip = ""
            most_frequent_ip_cnt = 0
            for ip, cnt in Dict.iterable(tempdict):
                if cnt > most_frequent_ip_cnt:
                    most_frequent_ip = ip
                    most_frequent_ip_cnt = cnt

            if verbose:
                Print.rewrite()

            if most_frequent_ip and most_frequent_ip_cnt > 1:  # do not return empty or single-occurrence ip
                return most_frequent_ip
            raise LookupError("IP not found")
        else:
            return str(ipgetter.get_external_ip())

    @classmethod
    def check_response(
        cls,
        endpoint: str,
        good_response: Union[str, bytes, list[Union[str, bytes]], tuple[Union[str, bytes], ...]],
        timeout: int = 10,
        debug: bool = False
    ) -> bool:
        """Check whether an endpoint response matches expected content."""
        if not isinstance(good_response, (str, bytes, list, tuple)):
            raise TypeError(f"good_response must be bytes, list or tuple, got '{type(good_response)}' instead")

        good_response_bytes: Union[bytes, list[bytes]]
        if isinstance(good_response, str):
            good_response_bytes = bytes(good_response, encoding="utf-8")
        elif isinstance(good_response, list) or isinstance(good_response, tuple):
            good_response_bytes = cast(list[bytes], List.apply_lambda_to_all_elements(good_response, bytes))
        else:
            good_response_bytes = good_response

        output: bool = False
        try:
            response = requests.get(endpoint, timeout=timeout)
            content = cast(bytes, response.content)
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
            if debug:
                Print.debug(e)
            return False
        if isinstance(good_response_bytes, bytes):
            output = content == good_response_bytes
        elif isinstance(good_response_bytes, list):
            output = content in good_response_bytes
        if debug and not output:
            Print.debug(
                f"Status: {response.status_code}",
                f"Content: {content!r}",
                f"Expected: {good_response_bytes!r}"
            )
        return output

    @classmethod
    def check_internet_apple(cls, timeout: int = 10, debug: bool = False) -> bool:
        """Check internet connectivity using Apple's captive portal endpoint."""
        return cls.check_response("http://captive.apple.com/hotspot-detect.html",
                                  (b'<HTML><HEAD><TITLE>Success</TITLE></HEAD><BODY>Success</BODY></HTML>\n',
                                   b'<HTML><HEAD><TITLE>Success</TITLE></HEAD><BODY>Success</BODY></HTML>'),
                                  timeout=timeout, debug=debug)

    @classmethod
    def check_internet_microsoft(cls, timeout: int = 10, debug: bool = False) -> bool:
        """Check internet connectivity using Microsoft's NCSI endpoint."""
        return cls.check_response("http://www.msftncsi.com/ncsi.txt",
                                  b'Microsoft NCSI',
                                  timeout=timeout, debug=debug)

    @classmethod
    def check_internet_microsoft_connect(cls, timeout: int = 10, debug: bool = False) -> bool:
        """Check internet connectivity using Microsoft's connect test endpoint."""
        return cls.check_response("http://www.msftconnecttest.com/connecttest.txt",
                                  b'Microsoft Connect Test',
                                  timeout=timeout, debug=debug)

    @classmethod
    def check_internet_google(cls, timeout: int = 10, debug: bool = False) -> bool:
        """Check internet connectivity using Google's generate_204 endpoint."""
        try:
            response = requests.get("http://connectivitycheck.gstatic.com/generate_204", timeout=timeout)
            output = bool(response.status_code == 204 and response.content == b'')
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
            if debug:
                Print.debug(e)
            return False
        if debug and not output:
            Print.debug(f"Status: {response.status_code}, Content: {response.content}")
        return output

    @classmethod
    def check_internet_firefox(cls, timeout: int = 10, debug: bool = False) -> bool:
        """Check internet connectivity using Firefox's captive portal endpoint."""
        return cls.check_response("http://detectportal.firefox.com/success.txt",
                                  b'success\n',
                                  timeout=timeout, debug=debug)

    @classmethod
    def request(
        cls,
        url: str,
        method: str,
        params: Optional[Any] = None,
        basic_auth_user: Optional[str] = None,
        basic_auth_password: Optional[str] = None,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        headers: Optional[Any] = None,
        **kwargs: Any
    ) -> Any:
        """Perform an HTTP request with optional auth and parameters."""
        auth = None
        if basic_auth_user and basic_auth_password:
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
    def get(
        cls,
        url: str,
        params: Optional[Any] = None,
        basic_auth_user: Optional[str] = None,
        basic_auth_password: Optional[str] = None,
        headers: Optional[Any] = None,
        **kwargs: Any
    ) -> Any:
        """Perform a GET request."""
        return cls.request(url=url, method="get", params=params, basic_auth_user=basic_auth_user,
                           basic_auth_password=basic_auth_password, headers=headers, **kwargs)

    @classmethod
    def post(
        cls,
        url: str,
        params: Optional[Any] = None,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        basic_auth_user: Optional[str] = None,
        basic_auth_password: Optional[str] = None,
        headers: Optional[Any] = None,
        **kwargs: Any
    ) -> Any:
        """Perform a POST request."""
        return cls.request(url=url, method="post", params=params, basic_auth_user=basic_auth_user,
                           basic_auth_password=basic_auth_password, data=data, json=json, headers=headers, **kwargs)

    @classmethod
    def delete(
        cls,
        url: str,
        params: Optional[Any] = None,
        basic_auth_user: Optional[str] = None,
        basic_auth_password: Optional[str] = None,
        headers: Optional[Any] = None,
        **kwargs: Any
    ) -> Any:
        """Perform a DELETE request."""
        return cls.request(url=url, method="delete", params=params, basic_auth_user=basic_auth_user,
                           basic_auth_password=basic_auth_password, headers=headers, **kwargs)


class _DualMethod:
    def __init__(self, instance_attr: str, class_attr: str) -> None:
        self._instance_attr = instance_attr
        self._class_attr = class_attr

    def __get__(self, instance: Any, owner: type) -> Any:
        if instance is None:
            return getattr(owner, self._class_attr)
        return getattr(instance, self._instance_attr)


Network.ping = _DualMethod("_ping_instance", "_ping_class")
Network.get_ip = _DualMethod("_get_ip_instance", "_get_ip_class")
Network.get_fqdn = _DualMethod("_get_fqdn_instance", "_get_fqdn_class")
