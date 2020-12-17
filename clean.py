import os
import sys
from godaddypy import Client, Account
from configparser import ConfigParser
import logging

script_dir = os.path.dirname(os.path.realpath(__file__))

config = ConfigParser()
try:
    config.read(script_dir + "/config.ini")
except Exception as err:
    sys.exit(f"Config parse: {err}")

API_KEY = os.getenv('GDKEY')
API_SECRET = os.getenv('GDSECRET')
CERTBOT_DOMAIN = os.getenv('CERTBOT_DOMAIN')

LOG_FILE = script_dir + "/clean.log"

if os.path.exists(LOG_FILE):
    os.remove(LOG_FILE)

logging.basicConfig(format = '%(levelname)-8s [%(asctime)s] %(message)s', level = logging.ERROR, filename = LOG_FILE)

try:
    my_acct = Account(api_key=API_KEY, api_secret=API_SECRET)
    client = Client(my_acct)
except Exception as err:
    logging.error(f"Account config error: {err}")

try:
    client.delete_records(CERTBOT_DOMAIN, name=f'_acme-challenge')
except Exception as err:
    logging.error(f"client.delete_records error: {err}")