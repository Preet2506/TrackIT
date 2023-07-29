from playwright.sync_api import sync_playwright
from config import proxy
from threading import Semaphore
import config

browser_semaphore = Semaphore(config.semaphore_values["SafeExpress"])

def trackSafeExpress(tkno):
    if (browser_semaphore._value == 0):
        return "no browser"
    with sync_playwright() as pl:
        browser_semaphore.acquire()
         
        pr = proxy()

        browser = pl.chromium.launch(headless=False)

        context = browser.new_context()

        # context.setDefaultTimeout(10000)

        page = context.new_page()
        
        try:
            page.goto('http://www.safexpress.com/index.html')

            page.fill('//input[@id="srchIt"]' , f'{tkno}')
            page.click('//input[@class="button big"]')

            data = page.inner_html('//div[@class="track-outer"]')
            print(data)

            # data2 = page.inner_html('//div[@id="pt1:pgl0"]')
            # data3 = page.inner_html('//div[@id="pt1:pgl3"]')
            # data4 = page.inner_html('//div[@id="pt1:pgl15"]')
            # data5 = page.inner_html('//div[@id="pt1:pgl4"]')
            # data6 = page.inner_html('//div[@id="pt1:pgl5"]')
            # print(data2,"\n",data3,"\n",data4,"\n",data5,"\n",data6,"\n")

            # data=[data7,data2,data3,data4,data5,data6]
            browser_semaphore.release()
            return data
        except:
            browser_semaphore.release()
            return "there has been some error"

