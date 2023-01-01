from playwright.sync_api import sync_playwright
from imap_tools import MailBox
import json
import random
from pathlib import Path
import os


class Marketplace():
    def __init__(self, proxy=None, viewport=None):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.firefox.launch(headless=False)
        self.context = self.browser.new_context(proxy={"server": f"{proxy.split(':')[0]}:{proxy.split(':')[1]}", "username": proxy.split(":")[2], "password": proxy.split(":")[3]} if proxy else None)
        self.page = self.context.new_page()
        if viewport:
            self.page.set_viewport_size(viewport)
        self.wait_time = {
            "min": 1000,
            "max": 3000
        }


    def is_captcha(self):
        try:
            self.page.locator("id=captcha_container").wait_for(state="visible", timeout=10000)
        except:
            return False
        else:
            return True


    def is_error(self):
        try:
            self.page.locator("css=div[id='error_box']").wait_for(state="attached", timeout=10000)
        except:
            return False
        else:
            return True


    def login(self, username=None, password=None, cookies=None):
        
        if cookies:
            self.context.add_cookies(json.loads(cookies))
            self.page.goto("https://www.facebook.com/", wait_until='networkidle')
        else:
            self.page.goto("https://www.facebook.com/", wait_until='networkidle')

            # Username
            self.page.wait_for_timeout(random.randint(3000, 5000))
            self.page.locator("css=input[id='email']").type(username, delay=200)

            # Password
            self.page.wait_for_timeout(random.randint(3000, 5000))
            self.page.locator("css=input[id='pass']").type(password, delay=200)
            
            # Login
            self.page.wait_for_timeout(random.randint(3000, 5000))
            self.page.locator("css=button[name='login']").click()
            
            # Check captcha
            if self.is_captcha():
                self.page.locator("id=captcha_container").wait_for(state="hidden", timeout=60000)

            # Check error
            if self.is_error():
                raise Exception(self.page.locator("css=div[id='error_box']").inner_text())

        # Ensure login
        self.page.locator("css=svg[aria-label='Your profile']").wait_for(state="attached")

        # save cookies for next login
        if not os.path.exists("inputs/cookies/"):
            os.mkdir("inputs/cookies")
        Path("inputs/cookies/"+username+".json").write_text(json.dumps(self.context.cookies()))
   

    def edit_profile(self, avatar=None, username=None, name=None, bio=None):
        # Profile
        # self.page.wait_for_timeout(random.randint(3000, 5000))
        self.page.locator("css=[data-e2e='profile-icon']").hover()
        self.page.locator("css=[data-e2e='profile-info']").click()

        # Edit profile
        # self.page.wait_for_timeout(random.randint(3000, 5000))
        self.page.locator("css=[data-e2e='edit-profile-entrance']").click()

        # Avatar
        if avatar:
            # self.page.wait_for_timeout(random.randint(3000, 5000))
            self.page.locator("css=[type='file']").set_input_files(avatar)
            self.page.locator("css=[class='e1gjao0r9 tiktok-xfwgx-Button-StyledBtn ehk74z00']").click()

        # Username
        if username:
            # self.page.wait_for_timeout(random.randint(3000, 5000))
            username_input = self.page.locator("css=[data-e2e='edit-profile-username-input']").locator("css=input")
            username_input.fill("")
            username_input.type(username, delay=200)

        # Name
        try:
            if name:
                # self.page.wait_for_timeout(random.randint(3000, 5000))
                name_input = self.page.locator("css=[data-e2e='edit-profile-name-input']").locator("css=input")
                name_input.fill("")
                name_input.type(name, delay=200, timeout=3000)
                cooldown = False
        except:
            cooldown = True

        # Bio
        if bio:
           # self.page.wait_for_timeout(random.randint(3000, 5000))
           bio_input = self.page.locator("css=[data-e2e='edit-profile-bio-input']").locator("css=input")
           bio_input.fill("")
           bio_input.type(bio, delay=200)

        # Save
        # self.page.wait_for_timeout(random.randint(3000, 5000))
        self.page.locator("css=[data-e2e='edit-profile-save']").click()

        # Confirm
        if name and not cooldown or username:
            # self.page.wait_for_timeout(random.randint(3000, 5000))
            self.page.locator("css=[data-e2e='set-username-popup-confirm']").click()

        self.page.wait_for_timeout(5000)


    def search(self, username):
        # Search
        self.page.wait_for_timeout(random.randint(6000, 8000))
        self.page.locator("css=[data-e2e='search-user-input']").type(username + "\n", delay=200)

        # Profile
        self.page.wait_for_timeout(random.randint(6000, 10000))
        try:
            self.page.locator("css=[data-e2e='search-user-unique-id']", has_text=username).click(timeout=10000)
        except:
            self.page.goto("https://www.tiktok.com/@" + username)
