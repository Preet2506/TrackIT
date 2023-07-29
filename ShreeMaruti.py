import random
from playwright.sync_api import sync_playwright
from crackCaptcha import extractCaptcha
from config import proxy
import os
from threading import Semaphore
import config


browser_semaphore = Semaphore(config.semaphore_values["shreeMaruti"])

def deleteImage(path):
    image_path = path

    # Delete the image if it exists
    if os.path.exists(image_path):
        os.unlink(image_path)
        print(f'{image_path} deleted successfully')
    else:
        print(f'{image_path} does not exist')


def trackShreeMaaruti(tkno):
    if (browser_semaphore._value == 0):
        return "no browser"
    with sync_playwright() as pl:
        browser_semaphore.acquire()
        print(browser_semaphore._value)
        pr = proxy()
        browser = pl.chromium.launch(headless=False, slow_mo=1200)

        context = browser.new_context()

        page = context.new_page()

        try:
            page.goto('https://shreemaruti.com/')
            page.wait_for_selector('//div[@class="ant-drawer-body"]')
            page.click('//button[@class="ant-btn ant-btn-default close"]')


            page.fill('//input[@id="shipment_number"]',f'{tkno}')
            page.click('//div[@class="tab_content input_group"]/button[@class="ant-btn ant-btn-default btn btn_secondary"]')

            page.wait_for_event("popup")
            # cracking the captcha
            page_size = page.evaluate("""() => {
                        return {
                            width: document.documentElement.clientWidth,
                            height: document.documentElement.clientHeight
                        };
                    }""")

            # Calculate the coordinates and dimensions of the area to capture
            left = int(page_size['width'] * 0.25)
            top = int(page_size['height'] * 0.25)
            width = int(page_size['width'] * 0.5)
            height = int(page_size['height'] * 0.4)

            # Take a screenshot of the specified area
            screenshot = page.screenshot(clip={"x": left, "y": top, "width": width, "height": height})

            # Save the screenshot to a file
            # n = random.randint(0,1000)
            with open(f"D:\Web_Designing\P2_tracker\images\{tkno}1.png", "wb") as f:
                f.write(screenshot)
            # loc = page.locator('//img[@id="my-captcha-image"]')
            # screenshot = loc.screenshot()


            captcha = extractCaptcha(f"{tkno}1.png")
            deleteImage(f"D:\Web_Designing\P2_tracker\images\{tkno}1.png")
            # entering captcha in the text box
            page.fill('//input[@id="re_captcha"]' , captcha)
            page.click('//button[@class="ant-btn ant-btn-default btn btn_secondary"]')

            # check if the captcha is correct or not
            i =2
            while(i<7):
                if(page.locator('//div[@class="trackingInfoBlock"]').count()>0):
                    print('success')
                    break

                if(page.locator('//p[@class="ant-form-item-explain-error"]').count() > 0):
                    page.click('//img[@id="refresh-captcha"]')
                    page_size = page.evaluate("""() => {
                                    return {
                                        width: document.documentElement.clientWidth,
                                        height: document.documentElement.clientHeight
                                    };
                                }""")

                    # Calculate the coordinates and dimensions of the area to capture
                    left = int(page_size['width'] * 0.25)
                    top = int(page_size['height'] * 0.25)
                    width = int(page_size['width'] * 0.5)
                    height = int(page_size['height'] * 0.4)

                    # Take a screenshot of the specified area
                    screenshot = page.screenshot(clip={"x": left, "y": top, "width": width, "height": height})

                    # Save the screenshot to a file
                    n = random.randint(0, 1000)
                    with open(f"/home/tracking/images/{tkno}{i}.png", "wb") as f:
                        f.write(screenshot)
                    # loc = page.locator('//img[@id="my-captcha-image"]')
                    # screenshot = loc.screenshot()

                    captcha = extractCaptcha(f"{tkno}{i}.png")
                    deleteImage(f"/home/tracking/images/{tkno}{i}.png")
                    # entering captcha in the text box
                    page.fill('//input[@id="re_captcha"]', captcha)
                    page.click('//button[@class="ant-btn ant-btn-default btn btn_secondary"]')

                else:
                    break
                i=i+1
            if(i==7):
                return "error"

            data = page.inner_html('//div[@id="shipment_information"]')
            # print(data)

            page.close()
            browser_semaphore.release()

            return data
        
        except:
            browser_semaphore.release()
            return "There has been some error"

