from playwright.sync_api import sync_playwright
from config import proxy
import json
import re
from threading import Semaphore
import config


browser_semaphore = Semaphore(config.semaphore_values["dhl"])

def trackDHL(tkno):
    if (browser_semaphore._value == 0):
        return "no browser"
    
    with sync_playwright() as pl:
        browser_semaphore.acquire()

        pr = proxy()
        browser = pl.chromium.launch(headless=True, slow_mo=300, proxy={"server": f"http://{pr}"})

        context = browser.new_context(extra_http_headers={
            "user-agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        })

        # context.setDefaultTimeout(10000)

        page = context.new_page()

        try:
            page.goto('https://www.dhl.com/in-en/home.html')

            a = page.inner_html('//body')
            # print(a)

            page.wait_for_selector('//div[@id="onetrust-banner-sdk"]')
            page.click('//button[@id="onetrust-accept-btn-handler"]')

            page.wait_for_selector('//input[@id="c-voc-marketing-stage-tracking--input"]')
            page.fill('//input[@id="c-voc-marketing-stage-tracking--input"]', f'{tkno}')
            page.click('//button[@class="c-voc-tracking-bar--button js--tracking-bar--button base-button "]')

            '''getting the details of the consignment'''

            page.click('//button[@id="c-tracking-result--checkpoints-dropdown-button"]')
            data = page.inner_html('//div[@class="c-tracking-result--header l-grid "]/div[3]')
            data1 = page.inner_html('//div[@class="c-tracking-result--header l-grid "]/div[5]')
            # print(data)
            
            page.close()
            browser_semaphore.release()

            return {"d1":data,"d2":data1}
        
        except:
            browser_semaphore.release()
            return "there has been some error"


# data = trackDHL(2505336186)



