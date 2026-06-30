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
        await page.wait_for_timeout(5000)

        await page.screenshot(path=r"C:\Users\Asus\Desktop\google-forms-bot\debug.png")

        selectors = [
            'div[role="listitem"]',
            '.Qr7Oae',
            'form',
            '[role="list"]',
            '.freebirdFormviewerViewItemList',
            '.geS5n',
            'div[role="radio"]',
            'input',
            'textarea',
            '.M7eMe',
            '[role="heading"]',
            '.o3Dpx',
        ]
        for sel in selectors:
            count = await page.locator(sel).count()
            print(f"{sel}: {count}")

        title = await page.title()
        print(f"Title: {title}")

        html = await page.inner_html("body")
        print(f"Body HTML length: {len(html)}")

        # find question-like elements
        all_divs = page.locator("div")
        all_count = await all_divs.count()
        print(f"Total divs: {all_count}")

        # Print first 50 divs with their role attribute
        for i in range(min(50, all_count)):
            div = all_divs.nth(i)
            role = await div.get_attribute("role") or ""
            class_attr = await div.get_attribute("class") or ""
            text = (await div.inner_text())[:80] if await div.inner_text() else ""
            print(f"  Div {i}: role='{role}' class='{class_attr[:60]}' text='{text}'")

        await browser.close()

asyncio.run(debug())
