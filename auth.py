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
TTL = config.get('GENERAL', 'TTL')
SLEEP = int(config.get('GENERAL', 'SLEEP'))
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

try:
    client.add_record(CERTBOT_DOMAIN, {'data':CERTBOT_VALIDATION,'name':f'_acme-challenge.{CERTBOT_DOMAIN}','ttl':TTL, 'type':'TXT'})
except Exception as err:
    logging.error(f"client.add_record error: {err}")
    if "UNABLE_TO_AUTHENTICATE" in err:
        sys.exit(1)

resolver = dns.resolver.Resolver(configure = False)
resolver.nameservers = ['8.8.8.8']
while True:
    try:
        time.sleep(SLEEP)
        resolver.resolve(f'_acme-challenge.{CERTBOT_DOMAIN}', 'txt')
        break
    except Exception:
        pass