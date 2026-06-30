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

        item = page.locator('div[role="listitem"]').nth(1)
        full_html = await item.evaluate("el => el.outerHTML")
        print("== FULL HTML of question 2 ==")
        print(full_html)
        print("\n== Length:", len(full_html))

        # Find all radio-related elements
        for sel in ['div[role="radio"]', '[role="radio"]', 'input[type="radio"]', '.Od2TWd']:
            count = await page.locator(sel).count()
            print(f"\n{sel}: {count} on page")

        # Check the actual radio buttons on the page
        radios = page.locator('[role="radio"]')
        rcount = await radios.count()
        for i in range(rcount):
            html = await radios.nth(i).evaluate("el => el.outerHTML")
            aria = await radios.nth(i).get_attribute("aria-checked") or "none"
            text = await radios.nth(i).inner_text() or ""
            print(f"\nRadio {i}: aria-checked={aria}, text='{text}'")
            print(f"  HTML: {html[:300]}")

        await browser.close()

asyncio.run(debug())
