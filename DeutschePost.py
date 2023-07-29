from playwright.sync_api import sync_playwright
from config import proxy
from threading import Semaphore
import config

browser_semaphore = Semaphore(config.semaphore_values["DeutschePost"])

def trackDP(tkno):
    if (browser_semaphore._value == 0):
        return "no browser"

    with sync_playwright() as pl:
        browser_semaphore.acquire()

        pr = proxy()
        
        browser = pl.chromium.launch(headless=False )

        context = browser.new_context()

        # context.setDefaultTimeout(10000)

        page = context.new_page()
        
        try:
            page.goto('https://www.packet.deutschepost.com/webapp/public/packet_traceit.xhtml')

            page.fill('//input[@id="j_idt35:j_idt37:j_idt40:awb"]',f'{tkno}')
            page.click('//input[@class="submitButton"][@type="submit"]')


            data1 = page.text_content('//div[@class="gmpacketTraceItEvent clearfix"]')
            data2 = page.text_content('//div[@class="gmpacketTraceItHistoryTable"]')
            data3 = page.text_content('//div[@class="gmpacketTraceItDestinationFrom"]')
            data4 = page.text_content('//div[@class="gmpacketTraceItDestinationTo"]')
            data5 = page.text_content('//div[@class="gmpacketTraceItOtherInfo"]')


            # print(data1)

            data = {"data1" : [data1,data2,data3,data4,data5]}
            # print(data)
            browser_semaphore.release()
            return data
        except:
            browser_semaphore.release()
            return "There has been some error"

# trackDP('LY420986226DE')
