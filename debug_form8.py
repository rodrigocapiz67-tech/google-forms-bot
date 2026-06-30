import asyncio, random
from playwright.async_api import async_playwright

async def test_exact_flow():
    url = "https://docs.google.com/forms/d/e/1FAIpQLSd2dfzPPeg7NV06vJ_dWRtTqyzaN_Ys8d20Iy8lo6n-4OTwag/viewform"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(locale="es-MX", timezone_id="America/Mexico_City")
        page = await context.new_page()

        await page.goto(url, wait_until="networkidle")
        await asyncio.sleep(3)

        # Welcome Siguiente - using click_button logic from main script
        for sel in ['div[role="button"]:has-text("Siguiente")', 'span.NPEfkd:has-text("Siguiente")']:
            btn = page.locator(sel).first
            if await btn.count() > 0 and await btn.is_visible():
                await btn.click()
                print(f"Clicked welcome via: {sel}")
                break
        await asyncio.sleep(2)

        # Page 1: fill and advance
        items = page.locator('div[role="listitem"]')
        print(f"Page 1 items: {await items.count()}")

        # Find and click label
        label = page.locator('label[for]').first
        await label.click()
        await asyncio.sleep(0.5)
        radio = page.locator('[role="radio"]').first
        print(f"aria-checked: {await radio.get_attribute('aria-checked')}")

        # Try EVERY approach to click Siguiente
        print("\nTrying to click Siguiente...")
        for sel in [
            'div[role="button"]:has-text("Siguiente")',
            'span.NPEfkd:has-text("Siguiente")',
            '.lRwqcd div[role="button"]',
            'div.lRwqcd div[role="button"]',
        ]:
            btn = page.locator(sel).first
            count = await btn.count()
            vis = await btn.is_visible() if count > 0 else False
            text = (await btn.inner_text())[:30] if count > 0 else ""
            print(f"  {sel}: count={count}, visible={vis}, text='{text}'")
            if count > 0 and vis:
                print(f"  -> Clicking...")
                await btn.click(force=True)
                await asyncio.sleep(3)

                items_after = page.locator('div[role="listitem"]')
                new_count = await items_after.count()
                print(f"  -> Items after: {new_count}")
                if new_count > 2:
                    print("  -> PAGE ADVANCED!")
                    for i in range(new_count):
                        t = await items_after.nth(i).inner_text()
                        print(f"     {i}: {t[:60]}")
                    break
                else:
                    print("  -> Same page, trying next selector...")

        await browser.close()

asyncio.run(test_exact_flow())
