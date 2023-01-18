from helpers.data import ACCOUNTS, VIEWPORT, LISTINGS, USER_ID, GS_SA
from helpers.auth import Auth
from helpers.marketplace import Marketplace
from helpers.listing_helper import publish_listing
from datetime import datetime
import random
from loguru import logger

logger.add('logs.txt')
auth = Auth(USER_ID, GS_SA)
user = auth.get_features()
auth.login()

# index of col in headers
idx_total_run = auth.headers.index("total_run")+1
idx_run_limit = auth.headers.index("run_limit")+1

# If listings are empty stop the function
if not LISTINGS:
    logger.error(f"No items found")

# Loop through the accounts and post the listings
for account in ACCOUNTS:
    fb = Marketplace(proxy=account['proxy'], viewport=VIEWPORT)
    try:
        fb.login(username=account['login']['id'], password=account['login']['password'], cookies=account['cookies'])
        for file in LISTINGS:
            for item in file['items']:
                if not user['paid'] and int(auth.get_values(user['row'], idx_run_limit)) == 0: 
                    raise Exception("Trial session is over. It's high time to purchase! \nContact the developer: https://www.upwork.com/services/product/development-it-a-facebook-marketplace-automation-bot-auto-listing-auto-reply-bot-1506700857494228992?ref=project_share")
                     
                publish_listing(item, file['type'], fb.page) 

                if user['paid']:
                    auth.worksheet.update_cell(user['row'], idx_total_run, int(auth.get_values(user['row'], idx_total_run))+1)
                else:
                    auth.worksheet.update_cell(user['row'], idx_run_limit, int(auth.get_values(user['row'], idx_run_limit))-1)
                    auth.worksheet.update_cell(user['row'], idx_total_run, int(auth.get_values(user['row'], idx_total_run))+1)
    except Exception as e:
        logger.error(e)
        continue
    else:
        print(f"Successfully posted items on account: {account['login']['id']}")
    finally:
        fb.browser.close()
        fb.playwright.stop()