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

        # Try to click the radio button using different methods
        radio = page.locator('[role="radio"][aria-label="Si"]')
        print(f"Radio found: {await radio.count()}")
        print(f"Before click - aria-checked: {await radio.get_attribute('aria-checked')}")
        print(f"Before click - class: {await radio.get_attribute('class')}")

        # Method 1: click the label instead of the radio
        label = page.locator('label:has-text("Si")').first
        print(f"\nLabel 'Si' count: {await label.count()}")
        if await label.count() > 0:
            await label.click()
            await asyncio.sleep(1)
            print(f"After label click - aria-checked: {await radio.get_attribute('aria-checked')}")

        # Check if Siguiente works now
        print(f"\nChecking Siguiente button...")
        siguiente = page.locator('span.NPEfkd:has-text("Siguiente")').first
        print(f"Siguiente visible: {await siguiente.is_visible()}")

        # Check for validation errors
        alerts = page.locator('[role="alert"]')
        alert_count = await alerts.count()
        print(f"Alert elements: {alert_count}")
        for i in range(alert_count):
            text = await alerts.nth(i).inner_text()
            print(f"  Alert {i}: '{text}'")

        # Check page structure after interaction
        items = page.locator('div[role="listitem"]')
        print(f"\nListitems after interaction: {await items.count()}")
        for i in range(await items.count()):
            text = await items.nth(i).inner_text()
            print(f"  Item {i}: {text[:80]}")

        # Check if there's an error state on the radio group
        rg = page.locator('[role="radiogroup"]')
        rg_class = await rg.get_attribute("class") or ""
        print(f"\nRadiogroup class: {rg_class}")

        # Try clicking Siguiente
        await siguiente.click()
        await asyncio.sleep(3)

        new_url = page.url
        print(f"\nURL after Siguiente: {new_url}")
        items_after = page.locator('div[role="listitem"]')
        print(f"Listitems after Siguiente: {await items_after.count()}")
        for i in range(await items_after.count()):
            text = await items_after.nth(i).inner_text()
            print(f"  Item {i}: {text[:80]}")

        await browser.close()

asyncio.run(debug())
