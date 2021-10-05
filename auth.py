# cython: language_level=3

import os
import sys
import time
import json
from configparser import ConfigParser

from godaddypy import Client, Account
from tld import get_tld
from func import Func

try:
    if getattr(sys, 'frozen', False):
        script_dir = os.path.dirname(sys.executable)
    else:
        script_dir = os.path.dirname(os.path.realpath(__file__))
    config = ConfigParser()
    config.read(script_dir + os.sep + "config.ini")
except Exception as err:
    raise SystemExit(f"Config parse: {err}")

API_KEY = os.getenv('GDKEY')
API_SECRET = os.getenv('GDSECRET')
DNS_SERVER = config.get('GENERAL', 'DNS_SERVER').split(',')
TTL = int(config.get('GENERAL', 'TTL'))
SLEEP = int(config.get('GENERAL', 'SLEEP'))
CERTBOT_DOMAIN = os.getenv('CERTBOT_DOMAIN')
CERTBOT_VALIDATION = os.getenv('CERTBOT_VALIDATION')
CERTBOT_REMAINING = int(os.getenv('CERTBOT_REMAINING_CHALLENGES'))
VERBOSE = os.getenv('VERBOSE')


def main():
    try:
        if VERBOSE:
            print('Authorize API...')
        my_acct = Account(api_key=API_KEY, api_secret=API_SECRET)
        client = Client(my_acct)
    except Exception as err:
        if VERBOSE:
            print(f"api.authorize: {err}")
        raise Exception(f"api.authorize: {err}")

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
            client.add_record(main_domain, {'data':CERTBOT_VALIDATION,'name':f'_acme-challenge.{reg_domain}','ttl':TTL,'type':'TXT'})
        else:
            query_domain = f"{domain_object.domain}.{domain_object}"
            client.add_record(main_domain, {'data':CERTBOT_VALIDATION,'name':'_acme-challenge','ttl':TTL,'type':'TXT'})
    except Exception as err:
        raise Exception(f"client.add_record error: {err}")
        if "UNABLE_TO_AUTHENTICATE" in err:
            raise Exception("Unable to authenticate")

    verb = ''
    if VERBOSE:
        verb = True
    while True:
        rdata = Func.checkTXTRecord(DNS_SERVER, query_domain, verbose=verb)
        if rdata:
            break
        time.sleep(10)
    if CERTBOT_REMAINING == 0:
        if VERBOSE:
            print(f'Sleep for {SLEEP} seconds...')
        time.sleep(SLEEP)


if __name__ == '__main__':
    main()