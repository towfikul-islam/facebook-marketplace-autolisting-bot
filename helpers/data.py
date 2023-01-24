import json
from pathlib import Path
import os
from helpers.file_helper import read_file

LISTINGS = read_file(os.path.join(os.getcwd(), 'inputs', 'products.xlsx'), worksheet='items')
ACCOUNTS = []
SETTINGS = read_file(os.path.join(os.getcwd(), 'inputs', 'products.xlsx'), worksheet='settings')[0]
acc_info = read_file(os.path.join(os.getcwd(), 'inputs', 'products.xlsx'), worksheet='accounts')
GS_SA = json.loads(Path(os.path.join(os.getcwd(), 'helpers', 'gs_sa.json')).read_text())

for acc in acc_info:
    cookie_file = os.path.join(os.getcwd(), 'inputs', 'cookies', acc['mail'] + ".json")

    ACCOUNTS.append({
        **acc, 
        **{
            "proxy_address": f"{acc['proxy_ip']}:{acc['proxy_port']}:{acc['proxy_username']}:{acc['proxy_password']}" if acc['proxy_ip'] else None,
            "cookies": Path(cookie_file).read_text() if os.path.exists(cookie_file) else None
        }
    })