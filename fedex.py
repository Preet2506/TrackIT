from playwright.sync_api import sync_playwright
from config import proxy,version
from fake_useragent import UserAgent

def trackFedex(tkno):
    with sync_playwright() as pl:
        pr = proxy()
        v = version()
        browser = pl.chromium.launch(headless=False,slow_mo=1000,)

        # a = UserAgent(browsers=['chrome']).random
        context = browser.new_context(extra_http_headers={
            'user-agent' : f'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v} Safari/537.36'
        })

        page = context.new_page()
        page.add_init_script("""
                    navigator.webdriver = false
                    Object.defineProperty(navigator, 'webdriver', {
                    get: () => false
                    })
                    """)

        page.add_init_script('''
                        Object.defineProperty(navigator, 'plugins', {
                        get: () => [1, 2, 3, 4, 5]
                        })
                    ''')

        page.add_init_script('''
                                Object.defineProperty(window, 'chrome', {
                                get: () => "{}"
                                })
                            ''')

        page.add_init_script(f'''
                                    Object.defineProperty(navigator, 'userAgent', {{
                                    get: () => "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v} Safari/537.36"
                                        }})
                                ''')

        page.add_init_script('''
                                Object.defineProperty(Notification, 'permission', {
                                get: () => "default"
                                    })
                            ''')

        page.goto('https://www.fedex.com/en-in/home.html')
        try:
            if(page.locator('//div[@class="modal-dialog"]').count()>0):
                print('inside')
                page.wait_for_selector('//div[@id="fedexmodal"]')
                print('found id')
                page.click('//div[@id="fedexmodal"]/div/div/div/button/a')
                print('clicked')
                
            page.fill('//input[@id="trackingnumber"]' , f'{tkno}')
            print('entered')
            page.click('//button[@id="btnSingleTrack"]')
            print('clicked')

            # page.wait_for_selector('//div[@class="status-description"]')

            data = page.text_content('//span[@id="shipmentIdentifier"]')
            print(data)
            return data
        except Exception as ex:
            print(ex)
            return page.inner_html('//body')


# trackFedex('390503203633')
'''
import requests 

response = requests.get('https://www.fedex.com/fedextrack/?action=track&tracknumbers=390503203633&locale=en_in&cntry_code=in') 
print(response.json())

'''
