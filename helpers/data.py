import json
from pathlib import Path
import os

resources = json.loads(Path("inputs/config.json").read_text())
lines = [line for line in Path("inputs/accounts.txt").read_text().strip().split('\n')]

ITEM_FILES = [ {"name": filename, "path": f'{os.getcwd()}\\products\\{filename}'} for filename in os.listdir("products") if filename.endswith(f".{resources['input_format']}")]

if len(ITEM_FILES) == 0:
    raise Exception(f"No {resources['files']['input_format']} file found in the directory")

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
    
VIEWPORT = resources['screen_size'] if 'screen_size' in resources else None

