import socket
from typing import Optional

import requests
import ipaddress
import urllib3
from urllib3.exceptions import InsecureRequestWarning
import warnings

class Site(object):
    def __init__(self, hostname: str, url: str, protocols: list = ['https'], verify: bool = True, **kwargs):
        self.hostname = hostname
        self.url = url
        self.protocol = protocols
        self.verify = verify
        self.port = kwargs.get("port") if kwargs.get("port") else ""

    def __str__(self):
        if not self.port:
            return f"{self.url}"
        else:
            return f"{self.url}:{self.port}"

    def __repr__(self):
        return f"Site(hostname={self.hostname},protocol={self.protocol},verify={self.verify})"

    @staticmethod
    def __parse_protocol(protocol: str) -> Optional[int]:
        if protocol == "https":
            return 443
        elif protocol == "http":
            return 80
        elif protocol == "ssh":
            return 22
        elif protocol == "ftp":
            return 21
        else:
            return None

    @staticmethod
    def validate_ip_addr(ip_addr: str) -> any:
        try:
            return ipaddress.ip_address(ip_addr)
        except Exception:
            print(f"{ip_addr} is an invalid IP Address")
            return None

    def dns_lookup(self) -> list:
        try:
            ip_list = list()
            for protocol in self.protocol:
                if not self.port:
                    self.port = self.__parse_protocol(protocol=protocol)
                resp = socket.getaddrinfo(host=self.hostname, port=self.port)
                for item in resp:
                    ip_list.append(item[4][0])
            return list(set(ip_list))
        except Exception as err:
            print(err)
            return list()

    def web_check(self) -> int:
        try:
            urllib3.disable_warnings(InsecureRequestWarning)
            response = requests.request(
                method="GET",
                url=str(self),
                verify=self.verify
            )
            return response.status_code
        except Exception as err:
            print(err)
        finally:
            warnings.simplefilter("default", InsecureRequestWarning)
