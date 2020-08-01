from requests import status_codes
from checker.core.site import Site
from checker.core.advancedDNS import AdvancedDNS
from checker.config.confHandler import Config

from argparse import ArgumentParser

def checkArgs(args):
    conf = Config()    

    # Print Default DNS List
    if args.default_dns_list: 
        for provider in conf.getDNSServerList():
            print(f"* {provider.name}")
            for server in provider.servers:
                print(f"\t[+] {server}")
            print()

    # Print Config File
    if args.config_location:
        print(f"Config Location:\n\t{conf.getSystemLocation()}")

    if args.quick_dns_lookup:
        for site in conf.getSitesList():
            s = Site(
                hostname=site.hostname,
                url=site.url,
                protocols=site.protocols
            )
            print(f"* {site.alias}:")

            for ip in s.dnsLookup():
                print(f"\t[+] {ip}")

            print()
    
    if args.quick_web_check:
        for site in conf.getSitesList():
            s = Site(
                hostname=site.hostname,
                url=site.url,
                protocols=site.protocols
            )
            print(f"» {site.alias}:")
            print(f"\t • Status Code: {s.webCheck()}")
            print()

    if args.dns_search:
        print(f"Searching Domain(s): {args.dns_search}")
        nameservers = conf.getDNSServerListIPs()
        print(f"Using Nameserver(s): {nameservers}\n")
        for domain in args.dns_search:
            adns = AdvancedDNS(hostname=domain,nameservers=nameservers)
            print(f"Domain: {domain}")
            print(f"Response: {adns.specialRequest()}")
            print()

if __name__ == "__main__":
    
    parser = ArgumentParser()
    info_options = parser.add_argument_group("Info Options")
    info_options.add_argument("--default-dns-list",action="store_true",help="List all Default DNS Servers configured")
    info_options.add_argument("--config-location",action="store_true",help="Print Default DNS Servers config location")
    
    quick_options = parser.add_argument_group("Quick Options")
    quick_options.add_argument("--quick-dns-lookup",action="store_true",help="Quick DNS Lookup based on sites defined in config.")
    quick_options.add_argument("--quick-web-check",action="store_true",help="Quick web check based on sites defined in config.")

    dns_options = parser.add_argument_group("DNS Options")
    dns_options.add_argument("--dns-search",action="store",nargs='+',type=str,default='',help="Domain name input, returns list of IP addresses")

    args = parser.parse_args()

    checkArgs(args)
