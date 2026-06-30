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

        # Click Siguiente on welcome
        await page.locator('span.NPEfkd:has-text("Siguiente")').first.click()
        await asyncio.sleep(3)

        q = page.locator('div[role="listitem"]').nth(1)

        # TEST 1: label[for] selector
        labels = q.locator('label[for]')
        l_count = await labels.count()
        print(f"label[for] in question: {l_count}")
        if l_count > 0:
            label_html = await labels.first.evaluate("el => el.outerHTML")
            print(f"Label HTML: {label_html[:300]}")

        # TEST 2: label:has-text
        labels2 = q.locator('label:has-text("Si")')
        l2_count = await labels2.count()
        print(f"\nlabel:has-text('Si') in question: {l2_count}")

        # TEST 3: Try clicking via label[for] 
        if l_count > 0:
            # Check aria-checked before
            radio = q.locator('[role="radio"]').first
            print(f"\nBefore label click - aria-checked: {await radio.get_attribute('aria-checked')}")
            
            await labels.first.click()
            await asyncio.sleep(1)
            
            print(f"After label click - aria-checked: {await radio.get_attribute('aria-checked')}")
            
            # Try Siguiente
            sig = page.locator('span.NPEfkd:has-text("Siguiente")').first
            await sig.click()
            await asyncio.sleep(3)
            
            url = page.url
            print(f"URL: {url[:100]}")
            items = page.locator('div[role="listitem"]')
            ic = await items.count()
            print(f"Listitems after Siguiente: {ic}")
            for i in range(ic):
                t = await items.nth(i).inner_text()
                print(f"  {i}: {t[:60]}")

        await browser.close()

asyncio.run(debug())
