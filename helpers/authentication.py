import gspread


class Authentication():
    def __init__(self, user_id):
        self.gs_credentials = {
            "type": "service_account",
            "project_id": "sheets-automation-374019",
            "private_key_id": "e17622957c783d9ee457eccb9c17ee97a325b202",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDNuyUAWA65wv1s\ngNMrhwu6k430qQ4f33BkS0t/+kK2HviY/eHvx6RS5jak6yQoVhm84g1JlIX+Nj0G\n2Y0uRoEnU6pOjV1DoydXbo1sPVdLd/cTaC4+m18g0nQy14dVKp2/SxBcmMPZCXzj\n4Mb7+pHMNY+f7a8KbGfJ1bY45kGKaC09OK1att7paFNxEOP2hBcRuQLbeob+yDfR\nIEsS7cGz/RcKNiNHjVrvlWPRtQ3LVSWCYRlwvPSPcmclp6R+Iwmofb0dVMdqQbeV\nb90mXDqphQ4hqKXhAApFDwOTNHQGozKMqdQm8bIoavaa2+niG2YUyzDuE0GP+nvs\ne1LDBv35AgMBAAECggEAYzDuACJ0xx+6bEwYhI4SG5z0/pdb1gY2/ERJXKTe8Uwx\ndCJEgwVwtv+ELTOqNUB+HFGpMmbHy+9+sQTHSx53Ouzd2g3Sf7/0QfVtflh89Egc\n+mBqm4jx7rNJjxHXkDqB4C9i7iJBmy015/ECP49qKFlSrDs+//mQeQHvX7O0ufPt\n+TaQz5nRELtDYkyjuZyvAkrmwgtocOpqeqsvrciBZ3uh4AdBH504dZjlAOk9eWni\nKwF84QhACCgxSPgLX/cOFYJzNU5O7WIFADnhWJAr2q3YLofarUwYyNyBrFOMaTnX\nId6r7DovcPEfCJ/qLtTNLhdK8kz6BcNh7Wkh8u3ueQKBgQD/ebhsm0lNdsali1uv\nxoB91k0M01CTSHak/AHhNryiKwlH/GIWSbYWKhCH6zGu1/kjWCwX7VCnP8DtXEZF\nrZS9ny7xqu9jBESsit0XNhqhnVvOrFiPAKxf82elwAbyB4soeNmkZ//4a4RjJYEZ\nwy1Ail94LbKAbMP4eIPW7OgokwKBgQDOJ0czM0McBCMIBmgK1YONkufL3NFpbavQ\n6m3feVD4QfTJRagY7TJyCaTbLEBVauoZ0Jqq/5TukNiQL8737AiZ36kK7zMkn6pa\nb85XR+OU2AlmoqqTkcxQ+yHtBnO+htQ9o7PQ1ZiPX2bPqBzgXfAbcEv8mVxDcMjA\nyxGHLatSwwKBgG6XcICDUF4aNq/e/de/pEvVAxG0QEMhsUqGVQH7QfkpjCD/Xi6r\nxgkeOH2+EInRsGXee2f4MVvVO10E/t6W37aePCIdjvdcF6ZhjofHwguIJP/4l3WA\nIx5+LbYQxHDtVw40EnMbGjGdyXdp+tL+LI6t19ocXhM+Ai+Da/8UGwPFAoGAKnZm\nsQIfEZc8i/ud1JV0GmYm/pPGQpwHZunSpdQ8PFaBkC+b1z6MRHb+EPMFcVKrU5Pn\nN8+bIqSNJu3iCKkCgIdUL19jvmhw013yN4IkO1VgYlahIfJHDmsb6tGIZ7cn4mZk\ntGA6o1V4PM+Y2xIeUdiInkgMfAuwHh31x00927cCgYEAkBpB7id0LN8Bq/+ztwi8\nDCaFzJPNMYRFIv4xMzilvdBJnyCMxdrQncJCmEMuuhja+W/T8HhvrVzKQnYSvLay\nDG2Ql0wmemwGusRqKhGX0YBI7mAewEMZGBpAzE2eieAgDSPIg+lbt1N4umaO9ZyW\nfci2ekZGNzRtxBAOb7+rcds=\n-----END PRIVATE KEY-----\n",
            "client_email": "bot-743@sheets-automation-374019.iam.gserviceaccount.com",
            "client_id": "109917564476768369139",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/bot-743%40sheets-automation-374019.iam.gserviceaccount.com"
        }
        self.client = gspread.service_account_from_dict(self.gs_credentials)
        self.file = self.client.open('marketplace-bot')
        self.worksheet = self.file.worksheet('trial_logs')
        self.user_id = user_id

    def get_user(self):
        user_instance = self.worksheet.find(self.user_id) 

        if user_instance:
            return user_instance
        else:
            raise Exception('Could not find your software license \n Contact the developer.')

    def get_values(self, row, col=None):
        if col is None:
            return self.worksheet.row_values(row)

        if row is None:
            return self.worksheet.col_values(col=col)

        if row and col:
            return self.worksheet.cell(row, col).value


