
from ipaddress import ip_address
from sys import platform
import dns
import sys
import socket
from collections import namedtuple
from checker.core.site import Site

SystemDNS = namedtuple('SystemDNS',['platform','location','heading'])

class AdvancedDNS(Site):
    def __init__(self, hostname: str, url: str, servers: list = list()):
        super().__init__(hostname=hostname, url=url)

        self.servers = list()
        for ip in servers:
            if super().validateIPAddr(ip_addr=ip):
                self.servers.append(ip)
        # self.servers = servers

    def __repr__(self):
        return "AdvancedDNS(hostname={hostname}, url={url}, servers={servers})".format(
            hostname = self.hostname,
            url = self.url,
            servers = self.servers
        )

    def __systemDnsInfo(self, *args ,**kwargs) -> SystemDNS:
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
            raise ValueError("OS [{}] not supported.".format(platform_type))

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

    def defaultServers(self) -> list:
        dns_info = self.__systemDnsInfo()
        with open(dns_info.location, 'r') as dns_file:
            dns_config = dns_file.readlines()
            
            if (dns_info.platform == "darwin") or (dns_info.platform == "linux"):
                trimmed_config = self.__trimConfig_unix(dns_config)
                return trimmed_config

            elif (dns_info.platform == "win32"):
                trimmed_config = self.__trimConfig_win(dns_config)
                return trimmed_config

    def getServers(self) -> list:
        return self.servers
        