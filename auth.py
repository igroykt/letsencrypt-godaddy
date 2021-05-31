# cython: language_level=3

import os
import sys
from godaddypy import Client, Account
from configparser import ConfigParser
import time
import dns.resolver
from tld import get_tld


script_dir = os.path.dirname(os.path.realpath(__file__))


config = ConfigParser()


try:
    config.read(script_dir + "/config.ini")
except Exception as err:
    raise SystemExit(f"Config parse: {err}")


API_KEY = os.getenv('GDKEY')
API_SECRET = os.getenv('GDSECRET')
TTL = int(config.get('GENERAL', 'TTL'))
SLEEP = int(config.get('GENERAL', 'SLEEP'))
RETRIES = int(config.get('GENERAL', 'RETRIES'))
CERTBOT_DOMAIN = os.getenv('CERTBOT_DOMAIN')
CERTBOT_VALIDATION = os.getenv('CERTBOT_VALIDATION')


try:
    my_acct = Account(api_key=API_KEY, api_secret=API_SECRET)
    client = Client(my_acct)
except Exception as err:
    raise SystemExit(f"Account config error: {err}")


def checkTXTRecord(query_domain, main_domain):
    dns_list = []
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = ['8.8.8.8']
    answers = dns.resolver.resolve(main_domain, 'NS')
    for rdata in answers:
        rdata = str(rdata)[:-1]
        dns_list.append(rdata)
    dns_list.sort()
    new_dns_list = []
    resolver = dns.resolver.Resolver(configure=False)
    for item in dns_list:
        answers = dns.resolver.resolve(item, 'A')
        for rdata in answers:
            rdata = str(rdata)
            new_dns_list.append(rdata)
    resolver = dns.resolver.Resolver(configure=False)
    i = 1
    dns_size = len(new_dns_list)
    for server in new_dns_list:
        resolver.nameservers = [server]
        try:
            resolver.resolve(f'_acme-challenge.{query_domain}', 'TXT')
            return
        except dns.resolver.NXDOMAIN as err:
            if i >= dns_size:
                raise SystemExit(err)
            i += 1
            pass


if "*" in CERTBOT_DOMAIN:
    domain = CERTBOT_DOMAIN.split(".")[1:]
    domain = ".".join(domain)
else:
    domain = CERTBOT_DOMAIN


domain_object = get_tld(domain, fix_protocol=True, as_object=True)
main_domain = f"{domain_object.domain}.{domain_object}"


try:
    if domain_object.subdomain:
        reg_domain = f"{domain_object.subdomain}"
        query_domain = f"{domain_object.subdomain}.{domain_object.domain}.{domain_object}"
        client.add_record(CERTBOT_DOMAIN, {'data':CERTBOT_VALIDATION,'name':f'_acme-challenge.{reg_domain}','ttl':TTL,'type':'TXT'})
    else:
        query_domain = f"{domain_object.domain}.{domain_object}"
        client.add_record(CERTBOT_DOMAIN, {'data':CERTBOT_VALIDATION,'name':'_acme-challenge','ttl':TTL,'type':'TXT'})
except Exception as err:
    raise SystemExit(f"client.add_record error: {err}")
    if "UNABLE_TO_AUTHENTICATE" in err:
        raise SystemExit("Unable to authenticate")


i = 1
while i <= RETRIES:
    try:
        checkTXTRecord(query_domain, main_domain)
        break
    except Exception:
        i += 1
        time.sleep(SLEEP)
    finally:
        if i >= RETRIES:
            raise SystemExit(f"resolver.resolve error: Could not find validation TXT record {CERTBOT_DOMAIN}")