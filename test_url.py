import asyncio
from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://docs.google.com/forms/d/1EfDR6z4Mgmwul0GXrSBMMjJrQRD10BHQiW-o0rH2BzA/viewform', wait_until='networkidle', timeout=30000)
        await asyncio.sleep(5)
        print(f'URL: {page.url}')
        print(f'Title: {await page.title()}')
        items = page.locator('div[role="listitem"]')
        print(f'Items: {await items.count()}')
        btns = page.locator('div[role="button"]')
        btn_texts = []
        for k in range(await btns.count()):
            t = (await btns.nth(k).inner_text()).strip()
            if t:
                btn_texts.append(t)
        print(f'Buttons: {btn_texts}')
        await browser.close()

asyncio.run(test())
