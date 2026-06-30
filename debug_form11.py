import asyncio
from playwright.async_api import async_playwright

async def debug():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(locale="es-MX", timezone_id="America/Mexico_City")
        page = await context.new_page()

        url = "https://docs.google.com/forms/d/e/1FAIpQLSd2dfzPPeg7NV06vJ_dWRtTqyzaN_Ys8d20Iy8lo6n-4OTwag/viewform"
        await page.goto(url, wait_until="networkidle")
        await asyncio.sleep(3)

        # Welcome + Page 1
        await page.locator('div[role="button"]:has-text("Siguiente")').first.click()
        await asyncio.sleep(2)
        await page.locator('label[for]').first.click()
        await asyncio.sleep(0.5)
        await page.locator('div[role="button"]:has-text("Siguiente")').first.click()
        await asyncio.sleep(3)

        # We're on page 2 now
        items = page.locator('div[role="listitem"]')
        print(f"Page 2 items: {await items.count()}")
        
        for i in range(await items.count()):
            item = items.nth(i)
            text = await item.inner_text()
            cls = await item.get_attribute("class") or ""
            print(f"\n=== Item {i} ===")
            print(f"Class: {cls}")
            print(f"Text: {text[:100]}")

            # Check what interactive elements exist
            for name, sel in [
                ('radio', 'div[role="radio"]'),
                ('checkbox', 'div[role="checkbox"]'),
                ('label[for]', 'label[for]'),
                ('input[type=text]', 'input[type="text"]'),
                ('textarea', 'textarea'),
                ('listbox', 'div[role="listbox"]'),
                ('radiogroup', 'div[role="radiogroup"]'),
            ]:
                els = item.locator(sel)
                cnt = await els.count()
                if cnt > 0:
                    print(f"  {name}: {cnt}")
                    for j in range(min(cnt, 3)):
                        html = await els.nth(j).evaluate("e => e.outerHTML") if cnt > 0 else ""
                        print(f"    [{j}]: {html[:200]}")

        # Try filling page 2 and check what happens
        await asyncio.sleep(3)
        await browser.close()

asyncio.run(debug())
