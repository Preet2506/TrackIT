from playwright.sync_api import sync_playwright
from config import proxy,version
from fake_useragent import UserAgent

def test(v):
    with sync_playwright() as pl:
        pr = proxy()
        #v =version()
        browser = pl.chromium.launch(headless=True,slow_mo=1000,proxy={'server' : f'{pr}'})

        # a = UserAgent(browsers=['chrome']).random
        context = browser.new_context(extra_http_headers={
            'user-agent': f'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v} Safari/537.36'
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


        page.add_init_script('''
                            Object.defineProperty(Notification, 'permission', {
                            get: () => "default"
                                })
                        ''')

        page.goto('https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html')
        page.screenshot(path='/home/tracking/images/test.png')

        data = page.text_content('//body')

        print(data)
        return data


# test()
