import json
from pathlib import Path
import os
from helpers.file_helper import read_file

resources = json.loads(Path("helpers/config.json").read_text())
lines = [line for line in Path("inputs/accounts.txt").read_text().strip().split('\n')]
GS_SA = json.loads(Path("helpers/gs_sa.json").read_text())

ITEM_FILES = [ {"name": filename, "path": os.path.join(os.getcwd(), "inputs", filename)} for filename in os.listdir("inputs") if filename.endswith(f".{resources['input_format']}")]

if len(ITEM_FILES) == 0:
    raise Exception(f"No {resources['input_format']} file found in the directory")

ACCOUNTS = []
for line in lines:
    account = line.split(':')
    cookie_file = 'inputs/cookies/' + account[0] + ".json"

    ACCOUNTS.append({
        "login": {
            "id": account[0],
            "password": account[1],
        },
        "proxy": f"{account[2]}:{account[3]}:{account[4]}:{account[5]}" if len(account) > 2 else None,
        "cookies": Path(cookie_file).read_text() if os.path.exists(cookie_file) else None
    })

USER_ID = resources['user']
VIEWPORT = resources['screen_size'] if 'screen_size' in resources else None

def read_listings():
    data = []
    for filepath in ITEM_FILES:
        data.append({
            "type": filepath['name'].split('.')[0], 
            "items": read_file(filepath['path'], data_format='dict')
        })
    return data

LISTINGS = read_listings()
