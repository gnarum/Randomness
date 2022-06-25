#!/usr/bin/python3
import sys
import dns.query
import dns.zone
import dns.resolver

from colorama import Fore, Style
bracket = f"{Fore.BLUE}[{Fore.GREEN}*{Fore.BLUE}]{Style.RESET_ALL} "
bracket_err = f"{Fore.BLUE}[{Fore.RED}*{Fore.BLUE}]{Style.RESET_ALL} "
def drawLine():
    print ('-' * 75)
    
try:
    domain = (sys.argv[1])
except:
    print("[!] USAGE: python3 " + sys.argv[0] + " DOMAIN_NAME")
    sys.exit(0)

def resolveDNS(name):
    resolver = dns.resolver.Resolver()
    results = resolver.query(name , "A")
    return results

def getNS (domain):
    mapping = {}
    name_servers = dns.resolver.query(domain, 'NS')
    print ("\nThe name servers for " + domain + " are:")
    drawLine()
    for name_server in name_servers:
        A_records = resolveDNS(str(name_server))
        for item in A_records:
            answer = ','.join([str(item)])
        mapping[str(name_server)] = answer
        print (bracket, "{:30}".format(str(name_server).rstrip('.')), "{:15}".format(answer))       
    return mapping
    
def zoneXFR(server):
    try:
        zone = dns.zone.from_xfr(dns.query.xfr(str(server).rstrip('.'), domain))
    except Exception as e:
        print (bracket_err, f"{Fore.RED}Error:{Style.RESET_ALL}", e.__class__, e)
    else:
        print ("\nResults for",server, "\nZone origin:", str(zone.origin).rstrip('.'))
        drawLine()
        for host in zone:
            if str(host) != '@':
                A_records = resolveDNS(str(host) + "." + domain)
                for item in A_records:
                    answer = ','.join([str(item)])   
                print(bracket, "{:30}".format(str(host) + "." + domain), answer)
        drawLine()
        
name_servers = getNS(domain)
for server in name_servers:
    print ("\nAttempting zone transfers for", server,name_servers[server])
    zoneXFR(name_servers[server])
