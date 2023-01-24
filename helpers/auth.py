import gspread
import socket
from loguru import logger
import os

class Auth():
    def __init__(self, user_id, service_acc):
        self.client = gspread.service_account_from_dict(service_acc)
        self.file = self.client.open('marketplace-bot')
        self.worksheet = self.file.worksheet('auth')
        self.user_id = user_id
        self.user = None
        self.headers = self.worksheet.row_values(1)

    def get_user(self):
        user_instance = self.worksheet.find(self.user_id) 

        if user_instance:
            return user_instance
        else:
            logger.error('USER ID is not found!')
    
    def get_features(self):
        all = self.worksheet.get_all_records()
        sheet_instance = self.get_user()

        for u in all:
            if u['id'] == self.user_id:
                usr = {**u, **{
                    "row": sheet_instance.row,
                    "col": sheet_instance.col,
                }}
                self.user = usr
                return usr
                
    def login(self):
        error_text = "This machine is not registered under your software license! You've to purchase the MULTIPLE MACHINE feature."
        machine_id = self.user['machine_id']
        machines = [m.strip() for m in machine_id.split(';')]
        current_machine = socket.gethostname()

        if not machine_id:
            self.worksheet.update_cell(self.user["row"], self.headers.index("machine_id")+1, current_machine)  
            return True
        
        if current_machine not in machines:
            if self.user['multiple_machine']:
                machines.append(current_machine)
            else:
                logger.error(error_text)
        
        if self.user['machine_limit']:
            if len(machines) > self.user['machine_limit']:
                logger.warning(f"Machine limit exceeded! You can use this script in {self.user['machine_limit']} machine")
                os.system("pause")
                exit()

        self.worksheet.update_cell(self.user["row"], self.headers.index("machine_id")+1, '; '.join(machines)) 
        return True 


    def get_values(self, row, col=None):
        if col is None:
            return self.worksheet.row_values(row)

        if row is None:
            return self.worksheet.col_values(col=col)

        if row and col:
            return self.worksheet.cell(row, col).value


