from requests import status_codes
from checker.core.site import Site
from checker.core.advancedDNS import AdvancedDNS
from checker.config.confHandler import Config

if __name__ == "__main__":
    pass
    # cfg = Config()
    # print(cfg.read())
    # sites = readSites()
    # for site in sites["sites"]:
    #     s = Site(hostname=site["site"]["hostname"], url=site["site"]["url"])
    #     print("{alias} -- {hostname}".format(
    #         alias=site["site"]["alias"],
    #         hostname=site["site"]["hostname"]
    #     ))
    #     print("\tDNS Lookup: {}".format(s.dnsLookup()))
        
    #     status_code = s.webCheck()
    #     if status_code == 200:
    #         print("\tHost Status: {}".format(site["site"]["url"], "OK"))
    #     else: 
    #         print("\tHost Status: {}".format(site["site"]["url"], status_code))
        
    #     print()