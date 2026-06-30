import asyncio
from playwright.async_api import async_playwright

async def debug():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(
            "https://docs.google.com/forms/d/e/1FAIpQLSd2dfzPPeg7NV06vJ_dWRtTqyzaN_Ys8d20Iy8lo6n-4OTwag/viewform",
            wait_until="networkidle"
        )
        await asyncio.sleep(3)

        # Click Siguiente on welcome screen
        btn = page.locator('span.NPEfkd:has-text("Siguiente")').first
        if await btn.count() > 0:
            await btn.click()
            await asyncio.sleep(3)

        # Find all div[role="listitem"]
        items = page.locator('div[role="listitem"]')
        count = await items.count()
        print(f"Total listitems: {count}")

        for i in range(count):
            item = items.nth(i)
            inner = await item.inner_html()
            tag = await item.evaluate("el => el.tagName")
            cls = await item.get_attribute("class") or ""
            print(f"\n=== Listitem {i} ===")
            print(f"Class: {cls}")
            print(f"Inner HTML (first 2000 chars):")
            print(inner[:2000])

            # Check all descendant input/radio/checkbox/textarea
            elements = [
                ('radio', 'div[role="radio"]'),
                ('checkbox', 'div[role="checkbox"]'),
                ('input', 'input'),
                ('textarea', 'textarea'),
                ('listbox', 'div[role="listbox"]'),
                ('radiogroup', 'div[role="radiogroup"]'),
                ('label', 'label'),
                ('select', 'select'),
            ]
            for name, sel in elements:
                el_count = await item.locator(sel).count()
                if el_count > 0:
                    print(f"  {name}: {el_count}")
                    for j in range(min(el_count, 5)):
                        el = item.locator(sel).nth(j)
                        outer = await el.evaluate("el => el.outerHTML")
                        print(f"    [{j}]: {outer[:300]}")

        await browser.close()

asyncio.run(debug())
