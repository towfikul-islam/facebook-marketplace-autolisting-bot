import json
from pathlib import Path
import os
from helpers.file_helper import read_file

resources = json.loads(Path("helpers/config.json").read_text())
acc_info = read_file('inputs/products.xlsx', worksheet='accounts')

GS_SA = json.loads(Path("helpers/gs_sa.json").read_text())
USER_ID = resources['user']
VIEWPORT = resources['screen_size'] if 'screen_size' in resources else None
LISTINGS = read_file('inputs/products.xlsx', worksheet='items')
ACCOUNTS = []

for acc in acc_info:
    cookie_file = 'inputs/cookies/' + acc['mail'] + ".json"

    ACCOUNTS.append({
        **acc, 
        **{
            "proxy_address": f"{acc['proxy_ip']}:{acc['proxy_port']}:{acc['proxy_username']}:{acc['proxy_password']}" if len(acc) > 2 else None,
            "cookies": Path(cookie_file).read_text() if os.path.exists(cookie_file) else None
        }
    })

