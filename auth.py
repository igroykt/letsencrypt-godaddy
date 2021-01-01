import os
import sys
from godaddypy import Client, Account
from configparser import ConfigParser
import time
import logging
import dns.resolver

script_dir = os.path.dirname(os.path.realpath(__file__))

config = ConfigParser()
try:
    config.read(script_dir + "/config.ini")
except Exception as err:
    sys.exit(f"Config parse: {err}")

API_KEY = os.getenv('GDKEY')
API_SECRET = os.getenv('GDSECRET')
TTL = int(config.get('GENERAL', 'TTL'))
SLEEP = int(config.get('GENERAL', 'SLEEP'))
RETRIES = int(config.get('GENERAL', 'RETRIES'))
CERTBOT_DOMAIN = os.getenv('CERTBOT_DOMAIN')
CERTBOT_VALIDATION = os.getenv('CERTBOT_VALIDATION')

LOG_FILE = script_dir + "/auth.log"

if os.path.exists(LOG_FILE):
    os.remove(LOG_FILE)

logging.basicConfig(format = '%(levelname)-8s [%(asctime)s] %(message)s', level = logging.ERROR, filename = LOG_FILE)

try:
    my_acct = Account(api_key=API_KEY, api_secret=API_SECRET)
    client = Client(my_acct)
except Exception as err:
    logging.error(f"Account config error: {err}")

def domainTail(domain):
    domain = domain.split(".")
    domain = domain[:len(domain)-2]
    tmp = []
    for level in domain:
        if "*" not in level:
            tmp.append(level)
    domain = '.'.join(tmp)
    if domain:
        return domain
    return False
    
try:
    if len(CERTBOT_DOMAIN.split(".")) > 2:
        domain_tail = domainTail(CERTBOT_DOMAIN)
        client.add_record(CERTBOT_DOMAIN, {'data':CERTBOT_VALIDATION,'name':f'_acme-challenge.{domain_tail}','ttl':TTL,'type':'TXT'})
    else:
        client.add_record(CERTBOT_DOMAIN, {'data':CERTBOT_VALIDATION,'name':'_acme-challenge','ttl':TTL, 'type':'TXT'})
except Exception as err:
    logging.error(f"client.add_record error: {err}")
    if "UNABLE_TO_AUTHENTICATE" in err:
        sys.exit(1)

def mainDomainTail(domain):
    domain = domain.split(".")
    domain = domain[len(domain)-2:]
    tmp = []
    for level in domain:
        if "*" not in level:
            tmp.append(level)
    domain = '.'.join(tmp)
    if domain:
        return domain
    return False

def getDnsList():
    dns_list = []
    resolver = dns.resolver.Resolver(configure = False)
    resolver.nameservers = ['8.8.8.8']
    answers = dns.resolver.resolve(main_domain, 'NS')
    for rdata in answers:
        rdata = str(rdata)[:-1]
        dns_list.append(rdata)
    dns_list.sort()
    return dns_list

def genDnsList(dns_list):
    new_dns_list = []
    resolver = dns.resolver.Resolver(configure = False)
    for item in dns_list:
        answers = dns.resolver.resolve(item, 'A')
        for rdata in answers:
            rdata = str(rdata)
            new_dns_list.append(rdata)
    return new_dns_list

def resolveDomain(dns_list):
    time.sleep(SLEEP)
    resolver = dns.resolver.Resolver(configure = False)
    i = 1
    for server in dns_list:
        resolver.nameservers = [server]
        try:
            resolver.resolve(f'_acme-challenge.{CERTBOT_DOMAIN}', 'TXT')
            return True
        except dns.resolver.NXDOMAIN as err:
            if i >= dns_size:
                return False
            i += 1
            pass

if len(CERTBOT_DOMAIN.split(".")) > 2:
    main_domain = mainDomainTail(CERTBOT_DOMAIN)
else:
    main_domain = CERTBOT_DOMAIN
dns_list = getDnsList()
dns_ip_list = genDnsList(dns_list)
is_resolved = resolveDomain(dns_ip_list)
if not is_resolved:
    logging.error(f"resolver.resolve error: Could not find validation TXT record for {CERTBOT_DOMAIN}")
    raise Exception(f"resolver.resolve error: Could not find validation TXT record {CERTBOT_DOMAIN}")

'''resolver = dns.resolver.Resolver(configure = False)
if len(CERTBOT_DOMAIN.split(".")) > 2:
    main_domain = mainDomainTail(CERTBOT_DOMAIN)
else:
    main_domain = CERTBOT_DOMAIN
resolver = dns.resolver.Resolver(configure = False)
answers = dns.resolver.resolve(main_domain, 'NS')
dns = []
for rdata in answers:
    rdata = str(rdata)[:-1]
    dns.append(rdata)
dns.sort()
resolver.nameservers = [dns[0]]

n = 1
while n <= RETRIES:
    try:
        time.sleep(SLEEP)
        resolver.resolve(f'_acme-challenge.{CERTBOT_DOMAIN}', 'txt')
        break
    except Exception as err:
        logging.error(f"resolver.resolve error: {err}")
        n += 1
        pass
else:
    logging.error(f"resolver.resolve error: Could not find validation TXT record for {CERTBOT_DOMAIN}")
    raise Exception(f"resolver.resolve error: Could not find validation TXT record for {CERTBOT_DOMAIN}")'''