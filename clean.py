import os
import sys
import json
import time
from configparser import ConfigParser

from godaddypy import Client, Account
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
CERTBOT_DOMAIN = os.getenv('CERTBOT_DOMAIN')
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

    main_domain = Func.mainDomainTail(CERTBOT_DOMAIN)

    try:
        if VERBOSE:
            print('Extract all TXT records...')
        records = client.get_records(main_domain, record_type='TXT')
        results = Func.GD_findTXTID(records)
        for result in results:
            client.delete_records(main_domain, name=result)
    except Exception as err:
        raise Exception(f"client.delete_records error: {err}")


if __name__ == '__main__':
    main()