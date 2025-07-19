import asyncio
from playwright.async_api import async_playwright
import os

async def debug_page():
    # Set display for WSL
    os.environ['DISPLAY'] = ':0'
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        print("🔍 Navigating to requirements page...")
        await page.goto("https://ecommerce-with-stripe-six.vercel.app/prd")
        await page.wait_for_load_state('networkidle')
        
        # Click requirements button
        print("📋 Looking for requirements button...")
        try:
            button = page.locator("text='Let's start the QA Hackathon'")
            if await button.count() > 0:
                print("✅ Found requirements button, clicking...")
                await button.click()
                await page.wait_for_timeout(2000)
                print(f"🌐 Current URL: {page.url}")
            else:
                print("ℹ️ No requirements button found, already in app")
        except Exception as e:
            print(f"❌ Error with requirements button: {e}")
        
        # Debug page structure
        print("\n🔍 Analyzing page structure...")
        
        # Check various possible product selectors
        selectors_to_test = [
            ".product",
            "[data-testid='product']",
            ".product-card",
            ".product-item",
            "[class*='product']",
            "[class*='Product']",
            "article",
            ".card",
            "[data-product]",
            "div[class*='grid'] > div",
            "main div > div",
        ]
        
        for selector in selectors_to_test:
            try:
                count = await page.locator(selector).count()
                print(f"📊 '{selector}': {count} elements")
                if count > 0:
                    # Get the first element's structure
                    first_element = page.locator(selector).first
                    html = await first_element.inner_html()
                    print(f"   📝 First element HTML (truncated): {html[:200]}...")
            except Exception as e:
                print(f"   ❌ Error testing selector '{selector}': {e}")
        
        # Get page title and main content structure
        title = await page.title()
        print(f"\n📄 Page title: {title}")
        
        # Get main content structure
        try:
            main_content = await page.locator("main").inner_html()
            print(f"📝 Main content (first 500 chars): {main_content[:500]}...")
        except:
            body_content = await page.locator("body").inner_html()
            print(f"📝 Body content (first 500 chars): {body_content[:500]}...")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_page())
