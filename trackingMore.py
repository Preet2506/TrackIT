from playwright.sync_api import sync_playwright
from config import proxy

def trackingMore(tkno):
    with sync_playwright() as pl:
        pr = proxy()    
        browser = pl.chromium.launch(headless=True,slow_mo=1000 , proxy={'server' : f'{pr}'})

        context = browser.new_context()

        page = context.new_page()
        # page.add_init_script("""
        # navigator.webdriver = false
        # Object.defineProperty(navigator, 'webdriver', {
        # get: () => false
        # })
        # """)

        page.goto(f'https://www.trackingmore.com/track/en/{tkno}')

        data = page.text_content('//ul[@class="card-list"]')
        print(data)
        return data

#trackingMore('390503203633')
