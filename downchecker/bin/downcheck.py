from downchecker.core.site import Site
from downchecker.core.advancedDNS import AdvancedDNS
from downchecker.core.services.ssh import SSH
from downchecker.config.confHandler import Config

from argparse import ArgumentParser


def check_args(args):
    conf = Config()

    # Print Default DNS List
    if args.default_dns_list:
        for provider in conf.get_dns_server_list():
            print(f"» {provider.name}")
            for server in provider.servers:
                print(f"\t• {server}\n")

    # Print Config File
    if args.config_location:
        print(f"Config Location:\n\t{conf.get_system_location()}")

    if args.quick_dns_lookup:
        for site in conf.get_sites_list():
            s = Site(
                hostname=site.hostname,
                url=site.url,
                protocols=site.protocols
            )
            print(f"» {site.alias}:")

            for ip in s.dns_lookup():
                print(f"\t• {ip}\n")

    if args.quick_web_check:
        for site in conf.get_sites_list():
            s = Site(
                hostname=site.hostname,
                url=site.url,
                protocols=site.protocols
            )
            print(f"» {site.alias}:")
            print(f"\t • Status Code: {s.web_check()}\n")

    if args.dns_search:
        print(f"Searching Domain(s): {args.dns_search}")
        nameservers = conf.get_dns_server_list_ips()
        print(f"Using Nameserver(s): {nameservers}\n")
        for domain in args.dns_search:
            adns = AdvancedDNS(hostname=domain, nameservers=nameservers)
            print(f"Domain: {domain}")
            print(f"Response: {adns.special_request()}\n")

    if args.ssh_endpoints:
        ssh_port = args.ssh_port if args.ssh_port else 22
        print(f"Checking SSH for endpoint(s): {args.ssh_endpoints}")
        for endpoint in args.ssh_endpoints:
            ssh = SSH(endpoint=endpoint, port=ssh_port)
            print(f"{endpoint}: {'up' if ssh.check() else 'down'}")


def main():
    parser = ArgumentParser()

    subparser = parser.add_subparsers()
    dns_subparser = subparser.add_parser('dns', help="DNS Related Commands")
    dns_subparser.add_argument("-s", "--search", action="store", nargs='+', type=str, default='',
                               help="Domain name input, returns list of IP addresses", dest="dns_search")

    ssh_subparser = subparser.add_parser('ssh', help="SSH Related Commands")
    ssh_subparser.add_argument("-c", "--check", action="store", nargs='+', type=str, default='',
                               help="SSH host input, checks for valid ssh servers up", dest="ssh_endpoints")
    ssh_subparser.add_argument("-p", "--port", action="store", type=int, default=22,
                               help="SSH Port to check", dest="ssh_port")

    conf_subparser = subparser.add_parser('config', aliases=['conf'], help="Config Related Commands")
    conf_subparser.add_argument("--nameservers", action="store_true", help="List all Default DNS Servers configured",
                                dest="default_dns_list")
    conf_subparser.add_argument("--location", action="store_true", help="Print Default DNS Servers config location",
                                dest="config_location")

    quick_options = parser.add_argument_group("Quick Options")
    quick_options.add_argument("--quick-dns-lookup", action="store_true", default=False,
                               help="Quick DNS Lookup based on sites defined in config.")
    quick_options.add_argument("--quick-web-check", action="store_true", default=False,
                               help="Quick web check based on sites defined in config.")

    parser.set_defaults(
        dns_search=False,
        ssh_endpoints=False,
        default_dns_list=False,
        config_location=False
    )

    args = parser.parse_args()

    check_args(args)

if __name__ == "__main__":
    main()