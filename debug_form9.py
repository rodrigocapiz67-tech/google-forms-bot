import asyncio, random
from playwright.async_api import async_playwright

async def test():
    url = "https://docs.google.com/forms/d/e/1FAIpQLSd2dfzPPeg7NV06vJ_dWRtTqyzaN_Ys8d20Iy8lo6n-4OTwag/viewform"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(locale="es-MX", timezone_id="America/Mexico_City")
        page = await context.new_page()

        await page.goto(url, wait_until="networkidle")
        await asyncio.sleep(3)

        # Welcome
        btn = page.locator('div[role="button"]:has-text("Siguiente")').first
        print(f"Welcome btn visible: {await btn.is_visible()}")
        try:
            await btn.click(force=True, timeout=5000)
            print("Welcome click OK")
        except Exception as e:
            print(f"Welcome click ERROR: {e}")
        
        await asyncio.sleep(2)

        # Page 1
        items = page.locator('div[role="listitem"]')
        print(f"Items: {await items.count()}")

        # Fill radio
        label = page.locator('label[for]').first
        await label.click(force=True)
        await asyncio.sleep(0.5)

        # Try clicking Siguiente with EXACT same code as click_button
        print("\n=== Trying click_button logic ===")
        for sel in [
            'div[role="button"]:has-text("Siguiente")',
            'span.NPEfkd:has-text("Siguiente")',
            'button:has-text("Siguiente")',
        ]:
            try:
                btn = page.locator(sel).first
                count = await btn.count()
                print(f"  {sel}: count={count}")
                if count > 0:
                    print(f"    Clicking...")
                    await btn.click(force=True, timeout=5000)
                    print(f"    Click done")
                    await asyncio.sleep(3)
                    items2 = page.locator('div[role="listitem"]')
                    c2 = await items2.count()
                    print(f"    Items after: {c2}")
                    if c2 > 2:
                        print("    SUCCESS: Page advanced!")
                        for j in range(c2):
                            t = await items2.nth(j).inner_text()
                            print(f"      {j}: {t[:60]}")
                    else:
                        print("    FAIL: Same page")
                    break
            except Exception as e:
                print(f"    Error: {e}")

        await browser.close()

asyncio.run(test())
