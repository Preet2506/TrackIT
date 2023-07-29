from playwright.sync_api import sync_playwright
from config import proxy

def trackAsendia(tkno):
    with sync_playwright() as pl:
        pr = proxy()
        browser = pl.chromium.launch(headless=False,slow_mo=1500)

        context = browser.new_context()

        page = context.new_page()

        page.goto(f'https://a1.asendiausa.com/tracking/?trackingnumber={tkno}')


        data = page.inner_html('//div[@class="container mb-4 body-content"]')


        print(data)
        return data


