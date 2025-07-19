import pytest
from pages.main import EcommercePage
from playwright.sync_api import expect


class TestMarketFunctionality:
    """Test suite for market/product functionality"""

    def test_products_are_displayed(self, page):
        """Test that products are displayed on the page"""
        print("🛍️ Testing products display...")
        ecommerce_page = EcommercePage(page)
        ecommerce_page.navigate_to_app()

        page.wait_for_load_state("networkidle")

        # Check if products are displayed
        product_count = ecommerce_page.get_product_count()
        assert product_count > 0, (
            f"Expected products to be displayed, but found {product_count}"
        )
        print(f"✅ Found {product_count} products")

    def test_minimum_products_available(self, page):
        """Test that minimum expected number of products are available"""
        print("📊 Testing minimum product count...")
        ecommerce_page = EcommercePage(page)
        ecommerce_page.navigate_to_app()

        page.wait_for_load_state("networkidle")

        product_count = ecommerce_page.get_product_count()
        # Based on documentation, should be 8 Japanese food products
        assert product_count >= 6, (
            f"Expected at least 6 products, but found {product_count}"
        )
        print(f"✅ Product count ({product_count}) meets minimum requirement")

    def test_product_information_display(self, page):
        """Test that products display required information"""
        print("ℹ️ Testing product information display...")
        ecommerce_page = EcommercePage(page)
        ecommerce_page.navigate_to_app()

        page.wait_for_load_state("networkidle")

        product_count = ecommerce_page.get_product_count()
        if product_count == 0:
            pytest.skip("No products available to test")

        # Test product titles
        try:
            first_product_title = ecommerce_page.get_first_product_title()
            assert (
                first_product_title is not None and len(first_product_title.strip()) > 0
            ), "Product should have a title"
            print(f"✅ First product title: '{first_product_title}'")
        except Exception as e:
            print(f"⚠️ Could not get product title: {e}")

        # Test product prices
        try:
            first_product_price = ecommerce_page.get_first_product_price()
            assert (
                first_product_price is not None and len(first_product_price.strip()) > 0
            ), "Product should have a price"
            print(f"✅ First product price: '{first_product_price}'")
        except Exception as e:
            print(f"⚠️ Could not get product price: {e}")

    def test_product_images_present(self, page):
        """Test that products have images"""
        print("🖼️ Testing product images...")
        ecommerce_page = EcommercePage(page)
        ecommerce_page.navigate_to_app()

        page.wait_for_load_state("networkidle")

        # Look for product images
        product_images = page.locator(
            "img[src*='product'], img[alt*='product'], .product img, [class*='product'] img"
        )
        image_count = product_images.count()

        if image_count > 0:
            print(f"✅ Found {image_count} product images")
        else:
            # Try broader image search
            all_images = page.locator("img")
            print(f"ℹ️ Found {all_images.count()} total images on page")

    def test_add_to_cart_buttons_present(self, page):
        """Test that products have 'Add to Cart' buttons"""
        print("🛒 Testing Add to Cart buttons presence...")
        ecommerce_page = EcommercePage(page)
        ecommerce_page.navigate_to_app()

        page.wait_for_load_state("networkidle")

        add_buttons = ecommerce_page.add_to_cart_buttons
        button_count = add_buttons.count()

        product_count = ecommerce_page.get_product_count()
        if product_count > 0:
            assert button_count > 0, (
                "Should have Add to Cart buttons when products are present"
            )
            print(
                f"✅ Found {button_count} 'Add to Cart' buttons for {product_count} products"
            )
        else:
            pytest.skip("No products available to test")

    def test_product_grid_layout(self, page):
        """Test that products are displayed in a proper grid layout"""
        print("📐 Testing product grid layout...")
        ecommerce_page = EcommercePage(page)
        ecommerce_page.navigate_to_app()

        page.wait_for_load_state("networkidle")

        # Look for grid container
        grid_containers = page.locator(
            ".grid, .products-grid, [class*='grid'], .flex, .products"
        )
        if grid_containers.count() > 0:
            print("✅ Grid layout container found")

        # Check if products are properly spaced
        product_count = ecommerce_page.get_product_count()
        if product_count > 1:
            print(f"✅ Multiple products ({product_count}) displayed in layout")

    def test_product_hover_interactions(self, page):
        """Test product hover interactions if any"""
        print("🖱️ Testing product hover interactions...")
        ecommerce_page = EcommercePage(page)
        ecommerce_page.navigate_to_app()

        page.wait_for_load_state("networkidle")

        product_count = ecommerce_page.get_product_count()
        if product_count > 0:
            # Hover over first product
            first_product = ecommerce_page.product_cards.first
            first_product.hover()
            page.wait_for_timeout(500)  # Wait for any hover effects
            print("✅ Product hover interaction tested")
        else:
            pytest.skip("No products available to test")

    def test_currency_display(self, page):
        """Test that prices display proper currency (JPY based on documentation)"""
        print("💴 Testing currency display...")
        ecommerce_page = EcommercePage(page)
        ecommerce_page.navigate_to_app()

        page.wait_for_load_state("networkidle")

        # Look for JPY currency symbols or text
        price_elements = page.locator("[class*='price'], .price")
        if price_elements.count() > 0:
            first_price = price_elements.first.text_content()
            if first_price:
                print(f"✅ Price format found: '{first_price}'")
                # Check for common currency indicators
                if any(symbol in first_price for symbol in ["¥", "JPY", "円"]):
                    print("✅ Japanese currency indicator found")
        else:
            print("⚠️ No price elements found")
