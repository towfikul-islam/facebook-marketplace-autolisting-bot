# from multiprocessing import Process
from helpers.data import ACCOUNTS, VIEWPORT, ITEM_FILE
from helpers.marketplace import Marketplace
from helpers.listing_helper import update_listings
from helpers.file_helper import read_file, write_file
import json
import random
import os

# Read the listings file
listings = read_file(ITEM_FILE, data_format='dict')

# If listings are empty stop the function
if not listings:
    raise Exception(f"No item found in {ITEM_FILE}")

for account in ACCOUNTS:
    fb = Marketplace(proxy=account['proxy'], viewport=VIEWPORT)
    try:
        fb.login(username=account['login']['id'], password=account['login']['password'], cookies=account['cookies'])
        update_listings(listings=listings, type='item', page=fb.page)
        os.system('pause')
    except Exception as e:
        print(e)
        print(f"\n\n PROXY: {account['proxy']} \n ACCOUNT: {account['login']['id']} \n PASSWORD: {account['login']['password']} \n")
    else:
        print('Successfully connected')
    finally:
        fb.browser.close()
        fb.playwright.stop()