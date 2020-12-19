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
CERTBOT_ALL_DOMAINS = os.getenv('CERTBOT_ALL_DOMAINS').split(",")
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
    
for current_domain in CERTBOT_ALL_DOMAINS:
    try:
        current_domain = current_domain.strip()
        if len(current_domain.split(".")) > 2:
            domain_tail = domainTail(current_domain)
            if domain_tail:
                client.add_record(CERTBOT_DOMAIN, {'data':CERTBOT_VALIDATION,'name':f'_acme-challenge.{domain_tail}','ttl':TTL,'type':'TXT'})
            client.add_record(CERTBOT_DOMAIN, {'data':CERTBOT_VALIDATION,'name':f'_acme-challenge','ttl':TTL, 'type':'TXT'})
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

resolver = dns.resolver.Resolver(configure = False)
if len(CERTBOT_DOMAIN.split(".")) > 2:
    main_domain = mainDomainTail(CERTBOT_DOMAIN)
else:
    main_domain = CERTBOT_DOMAIN
resolver = dns.resolver.Resolver(configure = False)
answers = dns.resolver.resolve(main_domain, 'NS')
for rdata in answers:
    rdata = str(rdata)[:-1]
    break
resolver.nameservers = [rdata]

n = 1
while n <= RETRIES:
    try:
        time.sleep(SLEEP)
        results = resolver.resolve(f'_acme-challenge.{CERTBOT_DOMAIN}', 'txt')
        break
    except Exception as err:
        logging.error(f"resolver.resolve error: {err}")
        n += 1
        pass
else:
    logging.error("resolver.resolve error: Could not find validation TXT record.")
    raise Exception("resolver.resolve error: Could not find validation TXT record.")