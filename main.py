# from multiprocessing import Process
from helpers.data import ACCOUNTS, VIEWPORT, ITEM_FILES
from helpers.marketplace import Marketplace
from helpers.listing_helper import update_listings, generate_multiple_images_path
from helpers.file_helper import read_file, write_file
import os

# # images_path = ""

# for listing in read_file(ITEM_FILES[0]['path'], data_format='dict'):
#     images_path = generate_multiple_images_path(listing['photos'])
#     print(images_path)
    



        

# Read the listings file
listings = [{ "type": filepath['name'].split('.')[0], "data": read_file(filepath['path'], data_format='dict')} for filepath in ITEM_FILES]    
# If listings are empty stop the function
if not listings:
    raise Exception(f"No item found in {ITEM_FILES}")

for account in ACCOUNTS:
    fb = Marketplace(proxy=account['proxy'], viewport=VIEWPORT)
    try:
        fb.login(username=account['login']['id'], password=account['login']['password'], cookies=account['cookies'])
        for file in listings:
            update_listings(listings=file['data'], type=file['type'], page=fb.page) 
    except Exception as e:
        print(e)
        print(f"\n\n PROXY: {account['proxy']} \n ACCOUNT: {account['login']['id']} \n PASSWORD: {account['login']['password']} \n")
        with open("logs/error.txt", "a") as f:
            f.write(str(e))
        continue
    else:
        print('Successfully connected')
    finally:
        fb.browser.close()
        fb.playwright.stop()
        os.system('pause')