
from ipaddress import ip_address
from sys import platform
import dns
import sys
import socket
from collections import namedtuple
from checker.core.site import Site

import dns.resolver

SystemDNS = namedtuple('SystemDNS',['platform','location','heading'])

class AdvancedDNS(Site):
    def __init__(self, hostname: str, url: str ='', nameservers: list = list()):
        super().__init__(hostname=hostname, url=url)

        self.nameservers = list()
        for ip in nameservers:
            if super().validateIPAddr(ip_addr=ip):
                self.nameservers.append(ip)

    def __repr__(self):
        return f"AdvancedDNS(hostname={self.hostname}, url={self.url}, nameservers={self.nameservers})"

    def __platformDNSInfo(self, **kwargs) -> SystemDNS:
        platform_type = str()

        if kwargs.get('platform'):
            platform_type = kwargs.get('platform')
        else:
            platform_type = sys.platform

        if (platform_type == "darwin") or (platform_type == "linux"):
            sysDNS = SystemDNS(
                platform_type,
                "/etc/resolv.conf",
                "nameserver"
            )
            return sysDNS

        elif (platform_type == "win32"):
            print("Windows is not yet supported")
            return None

        else:
            raise ValueError(f"OS [{platform_type}] not supported.")

    def __trimConfig_unix(self, dns_config: list) -> list:
        """

        """
        nameservers = list()
        for line in dns_config:
            if line.startswith("#") or not line.startswith("nameserver"):
                continue
            else: 
                line = line.replace('\n','')
                line = line.replace('nameserver','')
                line = line.replace(' ','')
                if super().validateIPAddr(ip_addr=line):
                    nameservers.append(line)

        return nameservers
    
    def __trimConfig_win(self, dns_config: list) -> list:
        return list()

    def systemServers(self) -> list:
        """ List of system's DNS servers. """
        dns_info = self.__platformDNSInfo()
        with open(dns_info.location, 'r') as dns_file:
            dns_config = dns_file.readlines()
            
            if (dns_info.platform == "darwin") or (dns_info.platform == "linux"):
                trimmed_config = self.__trimConfig_unix(dns_config)
                return trimmed_config

            elif (dns_info.platform == "win32"):
                trimmed_config = self.__trimConfig_win(dns_config)
                return trimmed_config

    def getServers(self) -> list:
        return self.nameservers
        
    def specialRequest(self) -> list:
        addresses = list()

        resolver = dns.resolver.Resolver()
        resolver.nameservers = self.nameservers

        answers = resolver.resolve(self.hostname,'a')

        for item in answers:
            addresses.append(str(item)) 
            # Using the overleaded str to get only the IP Addresses

        return addresses
