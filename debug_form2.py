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
        await page.wait_for_timeout(8000)

        await page.screenshot(path=r"C:\Users\Asus\Desktop\google-forms-bot\debug2.png")

        list_el = page.locator('[role="list"]')
        count = await list_el.count()
        print(f"role=list elements: {count}")

        if count > 0:
            inner_html = await list_el.first.inner_html()
            print(f"\nInner HTML of role=list (first 4000 chars):")
            print(inner_html[:4000])

            children = list_el.first.locator('> *')
            child_count = await children.count()
            print(f"\nDirect children count: {child_count}")

            for i in range(child_count):
                child = children.nth(i)
                tag = await child.evaluate("el => el.tagName")
                role = await child.get_attribute("role") or ""
                cls = await child.get_attribute("class") or ""
                clss = await child.get_attribute("class") or ""
                text = (await child.inner_text())[:80] if await child.inner_text() else ""
                print(f"  Child {i}: <{tag}> role='{role}' class='{cls[:60]}' text='{text}'")

        # form element contents
        form_count = await page.locator('form').count()
        print(f"\nForm elements: {form_count}")
        if form_count > 0:
            form_html = await page.locator('form').first.inner_html()
            print(f"Form inner HTML (first 3000 chars):")
            print(form_html[:3000])

        await browser.close()

asyncio.run(debug())
