import asyncio
from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(locale="es-MX", timezone_id="America/Mexico_City")
        page = await context.new_page()

        await page.goto(
            "https://docs.google.com/forms/d/e/1FAIpQLSd2dfzPPeg7NV06vJ_dWRtTqyzaN_Ys8d20Iy8lo6n-4OTwag/viewform",
            wait_until="networkidle"
        )
        await asyncio.sleep(3)

        # Welcome Siguiente
        await page.locator('span.NPEfkd:has-text("Siguiente")').first.click()
        await asyncio.sleep(3)

        url1 = page.url
        items1 = page.locator('div[role="listitem"]')
        print(f"Items before: {await items1.count()}")
        for i in range(await items1.count()):
            print(f"  {i}: {(await items1.nth(i).inner_text())[:60]}")

        # Click label via Playwright
        label = page.locator('label[for]').first
        print(f"\nLabel found: {await label.count()}")
        print(f"Label visible: {await label.is_visible()}")

        await label.click()
        await asyncio.sleep(1)

        radio = page.locator('[role="radio"]').first
        checked = await radio.get_attribute('aria-checked')
        print(f"aria-checked after click: {checked}")

        # Siguiente
        sig = page.locator('span.NPEfkd:has-text("Siguiente")').first
        await sig.click()
        await asyncio.sleep(3)

        url2 = page.url
        items2 = page.locator('div[role="listitem"]')
        print(f"\nURL: {url1[:70]} -> {url2[:70]}")
        print(f"Items after: {await items2.count()}")
        for i in range(await items2.count()):
            print(f"  {i}: {(await items2.nth(i).inner_text())[:60]}")

        await browser.close()

asyncio.run(test())
