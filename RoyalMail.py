from playwright.sync_api import sync_playwright
from config import proxy,version
from fake_useragent import UserAgent
from test import test


def trackRoyalMail(tkno):
    with sync_playwright() as pl:
        pr = proxy()
        v = version
        browser = pl.chromium.launch(headless=True,slow_mo=2000,proxy = {'server' : f'{pr}'})

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

        page.goto('https://www.royalmail.com/track-your-item#')

        try:

            page.wait_for_selector('//div[@class="privacy_prompt_container"]')
            print('cookie found')
            page.click('//button[@id="consent_prompt_submit"]')
            print('cookis accepted')
            page.fill('//input[@id="barcode-input"]',f'{tkno}')
            print('filled details')
            page.click('//button[@id="submit"]')
            print('submitted')
            page.wait_for_selector('//div[@class="status-description"]/h2')
            data = page.inner_html('//body')
            print(data)
            return data

        except Exception as error:
            print(error)
            # print(page.inner_html('//body'))
            return page.inner_html('//body')


# trackRoyalMail('FF085522243GB')


