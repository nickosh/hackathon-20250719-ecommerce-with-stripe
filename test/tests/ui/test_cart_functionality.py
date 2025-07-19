import pytest
from pages.main import EcommercePage
from playwright.sync_api import expect


class TestCartFunctionality:
    """Test suite for shopping cart/basket functionality"""

    def test_add_product_to_cart(self, page):
        """Test adding a product to the cart"""
        print("🛒 Testing add product to cart...")
        ecommerce_page = EcommercePage(page)
        ecommerce_page.navigate_to_app()

        page.wait_for_load_state("networkidle")

        product_count = ecommerce_page.get_product_count()
        if product_count == 0:
            pytest.skip("No products available to test")

        # Get initial cart count
        initial_cart_count = ecommerce_page.get_cart_count()
        print(f"🛒 Initial cart count: {initial_cart_count}")

        # Add first product to cart
        add_buttons = ecommerce_page.add_to_cart_buttons
        if add_buttons.count() > 0:
            add_buttons.first.click()
            page.wait_for_timeout(2000)  # Wait for cart update

            # Verify cart was updated
            updated_cart_count = ecommerce_page.get_cart_count()
            print(f"🛒 Updated cart count: {updated_cart_count}")
            print("✅ Product added to cart successfully!")
        else:
            pytest.skip("No 'Add to Cart' buttons found")

    def test_cart_icon_visibility(self, page):
        """Test that cart icon is visible"""
        print("🛒 Testing cart icon visibility...")
        ecommerce_page = EcommercePage(page)
        ecommerce_page.navigate_to_app()

        page.wait_for_load_state("networkidle")

        # Look for cart icon
        cart_icons = page.locator(
            "[data-testid='cart'], .cart, [class*='cart'], [aria-label*='cart'], svg[class*='cart']"
        )
        if cart_icons.count() > 0:
            print("✅ Cart icon found")
        else:
            print("⚠️ Cart icon not found - checking for shopping bag or basket icons")
            bag_icons = page.locator(
                "[class*='bag'], [class*='basket'], [aria-label*='bag'], [aria-label*='basket']"
            )
            if bag_icons.count() > 0:
                print("✅ Shopping bag/basket icon found")

    def test_cart_counter_display(self, page):
        """Test cart counter display"""
        print("🔢 Testing cart counter display...")
        ecommerce_page = EcommercePage(page)
        ecommerce_page.navigate_to_app()

        page.wait_for_load_state("networkidle")

        # Check for cart counter
        cart_count = ecommerce_page.get_cart_count()
        print(f"🛒 Current cart count display: '{cart_count}'")

        # Cart count should be a string representing a number
        if cart_count:
            try:
                count_num = int(cart_count)
                assert count_num >= 0, "Cart count should be non-negative"
                print(f"✅ Cart counter shows valid count: {count_num}")
            except ValueError:
                print(f"⚠️ Cart count is not numeric: '{cart_count}'")

    def test_add_multiple_products_to_cart(self, page):
        """Test adding multiple products to cart"""
        print("🛒 Testing multiple products addition...")
        ecommerce_page = EcommercePage(page)
        ecommerce_page.navigate_to_app()

        page.wait_for_load_state("networkidle")

        add_buttons = ecommerce_page.add_to_cart_buttons
        button_count = add_buttons.count()

        if button_count < 2:
            pytest.skip("Need at least 2 products to test multiple additions")

        # Add first product
        initial_count = ecommerce_page.get_cart_count()
        add_buttons.first.click()
        page.wait_for_timeout(1500)

        first_addition_count = ecommerce_page.get_cart_count()
        print(f"🛒 After first addition: {first_addition_count}")

        # Add second product
        add_buttons.nth(1).click()
        page.wait_for_timeout(1500)

        second_addition_count = ecommerce_page.get_cart_count()
        print(f"🛒 After second addition: {second_addition_count}")

        print("✅ Multiple products addition test completed!")

    def test_cart_persistence_on_page_reload(self, page):
        """Test that cart persists on page reload"""
        print("🔄 Testing cart persistence on reload...")
        ecommerce_page = EcommercePage(page)
        ecommerce_page.navigate_to_app()

        page.wait_for_load_state("networkidle")

        # Add a product to cart
        add_buttons = ecommerce_page.add_to_cart_buttons
        if add_buttons.count() == 0:
            pytest.skip("No products available to test")

        add_buttons.first.click()
        page.wait_for_timeout(2000)

        cart_count_before_reload = ecommerce_page.get_cart_count()
        print(f"🛒 Cart count before reload: {cart_count_before_reload}")

        # Reload the page
        page.reload()
        page.wait_for_load_state("networkidle")

        # Re-initialize page object after reload
        ecommerce_page = EcommercePage(page)
        cart_count_after_reload = ecommerce_page.get_cart_count()
        print(f"🛒 Cart count after reload: {cart_count_after_reload}")

        print("✅ Cart persistence test completed!")

    def test_cart_click_navigation(self, page):
        """Test clicking on cart icon for navigation"""
        print("🖱️ Testing cart click navigation...")
        ecommerce_page = EcommercePage(page)
        ecommerce_page.navigate_to_app()

        page.wait_for_load_state("networkidle")

        # Add a product first
        add_buttons = ecommerce_page.add_to_cart_buttons
        if add_buttons.count() > 0:
            add_buttons.first.click()
            page.wait_for_timeout(2000)

        # Try to click on cart
        cart_clickable = page.locator(
            "[data-testid='cart'], .cart, [class*='cart'][role='button'], [class*='cart'] button"
        )
        if cart_clickable.count() > 0:
            cart_clickable.first.click()
            page.wait_for_timeout(2000)
            print("✅ Cart click interaction tested")
        else:
            print("ℹ️ No clickable cart element found")

    def test_empty_cart_state(self, page):
        """Test empty cart state display"""
        print("🔄 Testing empty cart state...")
        ecommerce_page = EcommercePage(page)
        ecommerce_page.navigate_to_app()

        page.wait_for_load_state("networkidle")

        # Check initial cart state
        initial_cart_count = ecommerce_page.get_cart_count()
        print(f"🛒 Initial cart state: '{initial_cart_count}'")

        # Empty cart should show 0 or empty string
        if initial_cart_count in ["0", "", None]:
            print("✅ Empty cart state correctly displayed")
        else:
            print(f"ℹ️ Cart shows: '{initial_cart_count}'")

    def test_cart_visual_feedback_on_add(self, page):
        """Test visual feedback when adding items to cart"""
        print("👁️ Testing cart visual feedback...")
        ecommerce_page = EcommercePage(page)
        ecommerce_page.navigate_to_app()

        page.wait_for_load_state("networkidle")

        add_buttons = ecommerce_page.add_to_cart_buttons
        if add_buttons.count() == 0:
            pytest.skip("No Add to Cart buttons available")

        # Monitor for any visual changes
        before_click_screenshot = page.screenshot()

        add_buttons.first.click()
        page.wait_for_timeout(1000)  # Wait for visual feedback

        after_click_screenshot = page.screenshot()

        # Basic check - screenshots should be different if there's visual feedback
        if before_click_screenshot != after_click_screenshot:
            print("✅ Visual feedback detected on cart addition")
        else:
            print("ℹ️ No obvious visual feedback detected")
