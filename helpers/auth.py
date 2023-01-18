import gspread
import socket


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
            raise Exception('Could not find your software license \n Contact the developer.')
    
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
        error_text = "This machine is not registered! \nContact the developer: https://www.upwork.com/services/product/development-it-a-facebook-marketplace-automation-bot-auto-listing-auto-reply-bot-1506700857494228992?ref=project_share"
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
                raise Exception(error_text)
        
        self.worksheet.update_cell(self.user["row"], self.headers.index("machine_id")+1, '; '.join(machines)) 
        return True 


    def get_values(self, row, col=None):
        if col is None:
            return self.worksheet.row_values(row)

        if row is None:
            return self.worksheet.col_values(col=col)

        if row and col:
            return self.worksheet.cell(row, col).value


