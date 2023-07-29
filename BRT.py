from playwright.sync_api import sync_playwright
from config import proxy
from threading import Semaphore
import config

browser_semaphore = Semaphore(config.semaphore_values["BRT"])

def trackBRT(tkno):
    if (browser_semaphore._value == 0):
        return "no browser"
    with sync_playwright() as pl:
        browser_semaphore.acquire()

        pr = proxy()

        browser = pl.chromium.launch(headless=False,slow_mo=1000)

        context = browser.new_context()

        page = context.new_page()

        try:
            page.goto('https://services.brt.it/en/tracking')

            page.fill('//input[@id="CD"]' ,f'{tkno}')
            page.click('//input[@id="btnNext"]')

            page.click('//a[@class="btn btn-danger btn-maggiori"]')

            data = page.inner_html('//div[@class="brt-code"]')

            # print(data)
            browser_semaphore.release()
            return data
        except:
            browser_semaphore.release()
            return "there has been some error"


