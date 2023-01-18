# from multiprocessing import Process
from helpers.data import ACCOUNTS, VIEWPORT, ITEM_FILES
from helpers.authentication import Authentication
from helpers.marketplace import Marketplace
from helpers.listing_helper import publish_listing, generate_multiple_images_path
from helpers.file_helper import read_file, write_file
import os
import time
from datetime import datetime
import socket

auth = Authentication('test')
user = auth.get_user()
purchased = True if int(auth.get_values(user.row, 2)) == 1 else False


# Read the listings file
listings = [{ "type": filepath['name'].split('.')[0], "data": read_file(filepath['path'], data_format='dict')} for filepath in ITEM_FILES]    

# If listings are empty stop the function
if not listings:
    raise Exception(f"No item found in {ITEM_FILES}")

# Loop through the accounts and post the listings
for account in ACCOUNTS:
    fb = Marketplace(proxy=account['proxy'], viewport=VIEWPORT)
    try:
        fb.login(username=account['login']['id'], password=account['login']['password'], cookies=account['cookies'])
        for file in listings:
            for item in file['data']:
                if not purchased and int(auth.get_values(user.row, 3)) == 0: 
                    raise Exception("Trial session is over. It's high time to purchase! \nContact the developer: https://www.upwork.com/services/product/development-it-a-facebook-marketplace-automation-bot-auto-listing-auto-reply-bot-1506700857494228992?ref=project_share")
                    
                publish_listing(item, file['type'], fb.page) 

                if purchased:
                    auth.worksheet.update_cell(user.row, 4, int(auth.get_values(user.row, 4))+1)
                else: 
                    auth.worksheet.update_cell(user.row, 3, int(auth.get_values(user.row, 3))-1)
                    auth.worksheet.update_cell(user.row, 4, int(auth.get_values(user.row, 4))+1)
    except Exception as e:
        print(e)
        print(f"\n\n PROXY: {account['proxy']} \n ACCOUNT: {account['login']['id']} \n PASSWORD: {account['login']['password']} \n")
        with open("logs/error.txt", "a") as f:
            f.write(f'{str(e)} \n\n occured: {datetime.now()}')
        continue
    else:
        print(f"Successfully posted items on account: {account['login']['id']}")
    finally:
        fb.browser.close()
        fb.playwright.stop()