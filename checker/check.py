from requests import status_codes
from checker.core.site import Site
import yaml

def readSites():
    with open("/Users/Dan/Documents/Dev/Python/downchecker/config/sites.yml",'r') as sites_file:
        doc = yaml.load(
            stream=sites_file,
            Loader=yaml.FullLoader
        )
        return doc


if __name__ == "__main__":
    sites = readSites()
    for site in sites["sites"]:
        s = Site(hostname=site["site"]["hostname"], url=site["site"]["url"])
        print("{alias} -- {hostname}".format(
            alias=site["site"]["alias"],
            hostname=site["site"]["hostname"]
        ))
        print("\tDNS Lookup: {}".format(s.dnsLookup()))
        
        status_code = s.webCheck()
        if status_code == 200:
            print("\tHost Status: {}".format(site["site"]["url"], "OK"))
        else: 
            print("\tHost Status: {}".format(site["site"]["url"], status_code))
        
        print()