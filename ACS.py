from playwright.sync_api import sync_playwright
from config import proxy
from threading import Semaphore
import config

browser_semaphore = Semaphore(config.semaphore_values["ACS"])

def trackACS(tkno):
    if (browser_semaphore._value == 0):
        return "no browser"
    with sync_playwright() as pl:
        browser_semaphore.acquire()

        pr = proxy()
        
        browser = pl.chromium.launch(headless=False,slow_mo=4000)

        context = browser.new_context()

        page = context.new_page()

        try:
            page.goto('https://www.acscourier.net/en/myacs/my-shipments-reports/track-and-trace/')

            page.click('//a[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]')

            page.fill('//input[@id="mat-chip-list-input-0"]',f'{tkno}')
            page.click('//button[@class="btn btn-primary with-icon mt-0 px-3 ga-search-parcel-simple"][@type="submit"]')

            # page.wait_for_event("popup")

            page.wait_for_selector('//div[@class="table-wrapper ng-star-inserted"]')
            data= page.text_content('//app-parcels-search-results[@class="ng-star-inserted"]')

            data = {"data1" : data}
            # print(data)
            browser_semaphore.release()
            return data
        except:
            browser_semaphore.release()
            return "There has been some error"

# trackACS('9298469165')
