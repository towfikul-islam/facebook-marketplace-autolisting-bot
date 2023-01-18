from playwright.sync_api import sync_playwright
import json
import random
from pathlib import Path
import os


class Marketplace():
    def __init__(self, proxy=None, viewport=None):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.context = self.browser.new_context(proxy={"server": f"{proxy.split(':')[0]}:{proxy.split(':')[1]}", "username": proxy.split(":")[2], "password": proxy.split(":")[3]} if proxy else None)
        self.page = self.context.new_page()
        if viewport:
            self.page.set_viewport_size(viewport)

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
        self.page.locator("css=span", has_text="What's on your mind,").wait_for(state="attached", timeout=5000)

        # save cookies for next login
        if not os.path.exists("inputs/cookies/"):
            os.mkdir("inputs/cookies")
        Path("inputs/cookies/"+username+".json").write_text(json.dumps(self.context.cookies()))
