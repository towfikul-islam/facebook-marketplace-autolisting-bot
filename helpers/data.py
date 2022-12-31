import json
from pathlib import Path
import os

resources = json.loads(Path("inputs/config.json").read_text())
lines = [line for line in Path(resources['files']['accounts']).read_text().strip().split('\n')]

files = [filename for filename in os.listdir() if filename.endswith(f".{resources['input_format']}")]
if len(files) > 1:
    print(f"More than one {resources['files']['input_format']} file found in the directory")
    
    for idx, file in enumerate(files):
        print(f"\n IDX: {idx+1} ----- NAME: {file} \n")
    index = input("specify the file idx:\t")
    index = int(index.strip())
elif len(files) == 0:
    raise Exception(f"No {resources['files']['input_format']} file found in the directory")
else:
    index = 0

ITEM_FILE = files[index]

    
# ITEMS = Path("listings.csv").read_text()
# print(ITEMS)
print()


ACCOUNTS = []

for line in lines:
    account = line.split(':')
    cookie_file = resources['files']['cookies'] + account[0] + ".json"

    ACCOUNTS.append({
        "login": {
            "id": account[0],
            "password": account[1],
        },
        "proxy": f"{account[2]}:{account[3]}:{account[4]}:{account[5]}" if len(account) > 2 else None,
        "cookies": Path(cookie_file).read_text() if os.path.exists(cookie_file) else None
    })
    
VIEWPORT = resources['screen_size'] if 'screen_size' in resources else None

