import socket
import requests
import ipaddress

class Site(object):
    def __init__(self,hostname: str, url: str, protocols: list = ['https']):
        self.hostname = hostname
        self.url = url
        self.protocol = protocols

    def __repr__(self):
        return f"Site(hostname={self.hostname},protocol={self.protocol})"

    def __parseProtocol(self, protocol: str) -> int:
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

    def validateIPAddr(self, ip_addr: str) -> any:
        try:
            return ipaddress.ip_address(ip_addr)
        except:
            print(f"{ip_addr} is an invalid IP Address")
            return None
        

    def dnsLookup(self) -> list:
        try: 
            ip_list = list() 
            for protocol in self.protocol:
                port = self.__parseProtocol(protocol=protocol)
                resp = socket.getaddrinfo(host=self.hostname,port=port)
                for item in resp:
                    ip_list.append(item[4][0])
            return list(set(ip_list))
        except Exception as err:
            print(err)
            return list()

    def webCheck(self) -> int:
        try:
            response = requests.request(
                method="GET", 
                url=self.url
            )
            return response.status_code
        except Exception as err:
            print(err)