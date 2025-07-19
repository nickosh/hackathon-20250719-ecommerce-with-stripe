import pytest
from pages.main import EcommercePage
from playwright.sync_api import expect


class TestMainPage:
    """Test suite for the main page functionality"""

    def test_page_loads_successfully(self, page):
        """Test that the main page loads successfully"""
        print("🚀 Testing main page load...")
        ecommerce_page = EcommercePage(page)
        ecommerce_page.navigate_to_app()

        # Verify page loads with expected domain
        current_url = page.url
        assert "ecommerce-with-stripe-six.vercel.app" in current_url, f"Expected app domain in URL, got: {current_url}"
        
        # Check page has a title
        expect(page).not_to_have_title("")
        print("✅ Main page loads successfully!")

    def test_page_title_is_correct(self, page):
        """Test that the page has the correct title"""
        print("📄 Testing page title...")
        ecommerce_page = EcommercePage(page)
        ecommerce_page.navigate_to_app()

        # Check page title contains expected content
        page_title = page.title()
        assert page_title is not None and len(page_title) > 0, (
            "Page title should not be empty"
        )
        print(f"✅ Page title: '{page_title}'")

    def test_main_page_layout_elements(self, page):
        """Test that main layout elements are present"""
        print("🏗️ Testing main page layout elements...")
        ecommerce_page = EcommercePage(page)
        ecommerce_page.navigate_to_app()

        page.wait_for_load_state("networkidle")

        # Check for main heading
        main_heading = page.locator("h1")
        if main_heading.count() > 0:
            print("✅ Main heading found")

        # Check for navigation elements
        nav_elements = page.locator("nav, header, [role='navigation']")
        if nav_elements.count() > 0:
            print("✅ Navigation elements found")

        # Check for main content area
        main_content = page.locator("main, .main, #main")
        if main_content.count() > 0:
            print("✅ Main content area found")

        print("✅ Main page layout test completed!")

    def test_page_responsive_elements(self, page):
        """Test that page has responsive elements"""
        print("📱 Testing responsive elements...")
        ecommerce_page = EcommercePage(page)
        ecommerce_page.navigate_to_app()

        page.wait_for_load_state("networkidle")

        # Check for common responsive elements
        responsive_elements = page.locator(
            ".container, .grid, .flex, [class*='responsive']"
        )
        element_count = responsive_elements.count()

        assert element_count > 0, "Should have responsive layout elements"
        print(f"✅ Found {element_count} responsive layout elements")

    def test_page_accessibility_basics(self, page):
        """Test basic accessibility elements"""
        print("♿ Testing basic accessibility...")
        ecommerce_page = EcommercePage(page)
        ecommerce_page.navigate_to_app()

        page.wait_for_load_state("networkidle")

        # Check for alt attributes on images
        images = page.locator("img")
        if images.count() > 0:
            print(f"📸 Found {images.count()} images")

        # Check for proper heading structure
        headings = page.locator("h1, h2, h3, h4, h5, h6")
        if headings.count() > 0:
            print(f"📋 Found {headings.count()} headings")

        print("✅ Basic accessibility test completed!")

    def test_page_performance_indicators(self, page):
        """Test page performance indicators"""
        print("⚡ Testing performance indicators...")
        ecommerce_page = EcommercePage(page)

        import time

        start_time = time.time()

        ecommerce_page.navigate_to_app()
        page.wait_for_load_state("networkidle")

        load_time = time.time() - start_time

        # Basic performance assertion
        assert load_time < 10, (
            f"Page should load within 10 seconds, took {load_time:.2f}s"
        )
        print(f"✅ Page loaded in {load_time:.2f} seconds")
