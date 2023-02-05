from helpers.data import ACCOUNTS, LISTINGS, SETTINGS, GS_SA
from helpers.auth import Auth
from helpers.marketplace import Marketplace
from helpers.listing_helper import publish_listing
from loguru import logger
import os

contact_url = "https://www.upwork.com/services/product/development-it-a-facebook-marketplace-automation-bot-auto-listing-auto-reply-bot-1506700857494228992?ref=project_share"
logger.add('logs.txt')
auth = Auth(SETTINGS['user_id'], GS_SA)
user = auth.get_features()
auth.login()

# index of col in headers
idx_total_run = auth.headers.index("total_run")+1
idx_run_limit = auth.headers.index("run_limit")+1

# If listings are empty stop the function
if not LISTINGS:
    logger.error(f"No items found in the excel sheet")

# Loop through the accounts 
for acc_idx, account in enumerate(ACCOUNTS):
    if account['proxy_ip'] and not user['proxy']:
        logger.warning(f"Your are not allowed to use PROXY feature. Buy to activate!")
        account['proxy_address'] = None

    if acc_idx > 0 and not user['multiple_account']:
        logger.warning(f"Your are not allowed to use MULTIPLE FACEBOOK ACCOUNT feature. Buy to activate!")
        break

    fb = Marketplace(proxy=account['proxy_address'])

    try:
        fb.login(username=account['mail'], password=account['password'], cookies=account['cookies'])
        for item in LISTINGS:
            if not user['paid'] and int(auth.get_values(user['row'], idx_run_limit)) == 0: 
                logger.error(f"Trial session is over. It's high time to purchase!")
                break
                    
            publish_listing(item, fb.page, user, account, SETTINGS) 

            if user['paid']:
                auth.worksheet.update_cell(user['row'], idx_total_run, int(auth.get_values(user['row'], idx_total_run))+1)
            else:
                auth.worksheet.update_cell(user['row'], idx_run_limit, int(auth.get_values(user['row'], idx_run_limit))-1)
                auth.worksheet.update_cell(user['row'], idx_total_run, int(auth.get_values(user['row'], idx_total_run))+1)
    except Exception as e:
        logger.error(e)
        continue
    else:
        logger.success(f"Successfully posted items on account: {account['mail']}")
    finally:
        fb.browser.close()
        fb.playwright.stop()