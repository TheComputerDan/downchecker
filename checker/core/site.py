import socket
import requests
import ipaddress

class Site(object):
    def __init__(self,hostname: str, url: str, ports: list = [80,443]):
        self.hostname = hostname
        self.url = url
        self.ports = ports

    def __repr__(self):
        return "Site(hostname={},ports={})".format(
            self.hostname,
            self.ports
        )

    def validateIPAddr(self, ip_addr: str) -> any:
        try:
            return ipaddress.ip_address(ip_addr)
        except:
            print("{} -- is and invalid IP Address ".format(ip_addr))
            return None
        

    def dnsLookup(self) -> list:
        try: 
            ip_list = list() 
            for port in self.ports:
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