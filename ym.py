from playwright.sync_api import sync_playwright
from config import proxy
from threading import Semaphore
import config

browser_semaphore = Semaphore(config.semaphore_values["yanwen"])

def trackym(tkno):
    if (browser_semaphore._value == 0):
        return "no browser"
    with sync_playwright() as pl:
        browser_semaphore.acquire()

        pr = proxy()

        browser = pl.chromium.launch(headless=False , slow_mo=50 )

        context = browser.new_context()

        # context.setDefaultTimeout(10000)

        page = context.new_page()

        try:
            page.goto('https://track.yw56.com.cn/')

            page.click('//div[@class="qh_zy"]/a[@class="court"]')

            page.fill('//input[@id="numbers_en"]',f'{tkno}')
            page.click('//div[@class="input bx-relative"]/a/img')

            data1 = page.inner_html('//div[@class="cx_lb"]')
            # data2 = page.text_content('//div[@class="czhaodl"]')

            # print(data1)

            data = data1

            browser_semaphore.release()
            return data
        
        except:
            browser_semaphore.release()
            return "there has been some error"


