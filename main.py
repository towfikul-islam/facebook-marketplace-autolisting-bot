# from multiprocessing import Process
from helpers.data import ACCOUNTS, VIEWPORT, ITEM_FILE
from helpers.marketplace import Marketplace
from helpers.listing_helper import update_listings
from helpers.file_helper import get_data_from_csv
import json
import random

listings = get_data_from_csv(ITEM_FILE)

if not listings:
    raise Exception(f"No item found in {ITEM_FILE}")

for account in ACCOUNTS:
    fb = Marketplace(proxy=account['proxy'], viewport=VIEWPORT)

    try:
        fb.login(username=account['login']['id'], password=account['login']['password'], cookies=account['cookies'])
        # update_listings("")
    except Exception as e:
        print(e)
        print(f"\n\n PROXY: {account['proxy']} \n ACCOUNT: {account['login']['id']} \n PASSWORD: {account['login']['password']} \n")
    else:
        print('Successfully connected')
    finally:
        fb.browser.close()
        fb.playwright.stop()