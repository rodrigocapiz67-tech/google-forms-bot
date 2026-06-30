import asyncio
from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(locale="es-MX", timezone_id="America/Mexico_City")
        page = await context.new_page()

        await page.goto("https://docs.google.com/forms/d/e/1FAIpQLSd2dfzPPeg7NV06vJ_dWRtTqyzaN_Ys8d20Iy8lo6n-4OTwag/viewform", wait_until="networkidle")
        await asyncio.sleep(3)

        # Click welcome
        await page.locator('div[role="button"]:has-text("Siguiente")').first.click()
        await asyncio.sleep(3)

        # Click label  
        await page.locator('label[for]').first.click()
        await asyncio.sleep(0.5)

        # Check for validation errors or alerts
        alerts = page.locator('[role="alert"]')
        for i in range(await alerts.count()):
            text = await alerts.nth(i).inner_text()
            print(f"Alert {i}: '{text}'")
            html = await alerts.nth(i).inner_html()
            print(f"  HTML: {html[:200]}")

        # Check radio state
        radio = page.locator('[role="radio"]').first
        print(f"Radio checked: {await radio.get_attribute('aria-checked')}")
        
        # Check Siguiente button state
        btn = page.locator('div[role="button"]:has-text("Siguiente")').first
        print(f"Siguiente disabled: {await btn.get_attribute('aria-disabled')}")
        print(f"Siguiente class: {await btn.get_attribute('class')}")
        
        # Check form for error state
        form = page.locator('form')
        form_html = await form.first.inner_html()
        if 'error' in form_html.lower() or 'invalid' in form_html.lower():
            print("Form has error/invalid state")
        
        # Take screenshot
        await page.screenshot(path=r"C:\Users\Asus\Desktop\google-forms-bot\state.png")

        # Now try clicking Siguiente via evaluate
        result = await page.evaluate("""
            () => {
                const btns = document.querySelectorAll('div[role="button"]');
                for (const btn of btns) {
                    if (btn.textContent.trim() === 'Siguiente') {
                        btn.click();
                        return 'clicked';
                    }
                }
                return 'not found';
            }
        """)
        print(f"\nEvaluate click: {result}")
        await asyncio.sleep(3)
        
        items = page.locator('div[role="listitem"]')
        print(f"Items after evaluate click: {await items.count()}")
        for i in range(await items.count()):
            print(f"  {i}: {(await items.nth(i).inner_text())[:60]}")

        await browser.close()

asyncio.run(test())
