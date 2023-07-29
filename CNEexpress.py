from playwright.sync_api import sync_playwright
from config import proxy
from threading import Semaphore
import config

browser_semaphore = Semaphore(config.semaphore_values["CNE"])

def trackCNE(tkno):
    if (browser_semaphore._value == 0):
        return "no browser"
    with sync_playwright() as pl:
        browser_semaphore.acquire()

        pr =proxy()
        
        browser = pl.chromium.launch(headless=False )

        context = browser.new_context()

        # context.setDefaultTimeout(10000)

        page = context.new_page()

        try:
            page.goto('https://www.cne.com/English/')

            page.fill('//textarea[@type="search"]',f'{tkno}')
            page.click('//input[@class="fh-btn"]')

            data = page.inner_html('//section[@class="timeline_tracking_area"]')
            # data = {"data2" : data2}
            browser_semaphore.release()
            return data
        except:
            browser_semaphore.release()
            return "There has been some error"

# trackCNE('3A5V622967774')
