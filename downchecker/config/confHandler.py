from ipaddress import ip_address
from downchecker.core.site import Site
import os
import sys
import yaml
from collections import namedtuple
from pathlib import Path

ConfFile = namedtuple('ConfFile', ['directories', 'fullpath'])
ConfigSections = namedtuple('ConfigSections', ['sites', 'dnsproviders'])
# TODO Consider a different Name
SITE = namedtuple('SITE', ['alias', 'hostname', 'url', 'protocols'])
PROVIDER = namedtuple('PROVIDER', ['name', 'servers'])


class Config(object):
    def __init__(self, file: str = str()):
        self.file = file
        self.cwd = os.path.dirname(os.path.realpath(__file__))
        self.__initialize()

    def __initialize(self):
        platform_config_info = self.__platform_config()
        dirs = Path(platform_config_info.directories)
        cfg_file = Path(platform_config_info.fullpath)

        if not dirs.exists():
            dirs.mkdir(mode=0o755, parents=True)

        if not cfg_file.exists():
            cfg_file.touch(mode=0o644)

            base_config = Path(self.cwd + "/downchecker.yml")
            base_contents = list()

            with open(base_config,'r') as base:
                base_contents = base.readlines()

            with open(cfg_file, 'a') as conf_file:
                conf_file.writelines(base_contents)

    @staticmethod
    def __platform_config(**kwargs) -> ConfFile:
        platform_type = str()

        if kwargs.get('platform'):
            platform_type = kwargs.get('platform')
        else:
            platform_type = sys.platform

        if platform_type == "darwin":
            darwin_config = ConfFile(
                str(Path.home()) + "/.config/downchecker/",
                str(Path.home()) + "/.config/downchecker/downchecker.yml"
            )
            return darwin_config

        elif platform_type == "linux":
            linux_config = ConfFile(
                str(Path.home()) + "/.config/downchecker/",
                str(Path.home()) + "/.config/downchecker/downchecker.yml"
            )
            return linux_config

        elif platform_type == "win32":
            print("Windows is not yet supported")
            return None

    def getSystemLocation(self) -> str:
        return self.__platform_config().fullpath

    def getDNSServerList(self) -> list:
        default_dns_servers = self.read().dnsproviders
        return default_dns_servers
    
    def getDNSServerListIPs(self) -> list:
        ip_addresses = list()
        default_dns_servers = self.read().dnsproviders
        for provider in default_dns_servers:
            ip_addresses.extend(provider.servers)
        return ip_addresses

    def getSitesList(self) -> list:
        default_sites_list = self.read().sites
        return default_sites_list

    def read(self) -> ConfigSections:

        conf = self.__platform_config()

        sites_list = list() 
        dns_list = list() 

        with open(conf.fullpath,'r') as config_file:
            doc = yaml.load(
                stream=config_file,
                Loader=yaml.FullLoader
            )

            for site in doc["sites"]:
                site_item = SITE(
                    site["site"]["alias"],
                    site["site"]["hostname"],
                    site["site"]["url"],
                    site["site"]["protocols"]
                )
                sites_list.append(site_item)

            for dns in doc["dns"]:
                dns_item = PROVIDER(
                    dns["provider"]["name"],
                    dns["provider"]["servers"]
                )
                dns_list.append(dns_item)

            configuration = ConfigSections(
                sites= sites_list,
                dnsproviders = dns_list
            )

            return configuration