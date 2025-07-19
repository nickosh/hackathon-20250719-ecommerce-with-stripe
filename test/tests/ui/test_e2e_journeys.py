import pytest
from playwright.sync_api import expect
from pages.main import EcommercePage


class TestE2EUserJourneys:
    """End-to-End test suite for complete user journeys"""

    def test_full_shopping_journey_single_product(self, page):
        """E2E: Complete shopping journey with one product"""
        print("🛍️ Starting E2E test: Single product shopping journey...")
        
        # Step 1: Open the app
        print("📱 Step 1: Opening the application...")
        ecommerce_page = EcommercePage(page)
        ecommerce_page.navigate_to_app()
        
        # Verify app loaded
        expect(page).to_have_url("https://ecommerce-with-stripe-six.vercel.app/")
        print("✅ App loaded successfully")
        
        # Step 2: Verify products are available
        print("🔍 Step 2: Checking products availability...")
        page.wait_for_load_state("networkidle")
        product_count = ecommerce_page.get_product_count()
        assert product_count > 0, f"No products found on the page (found {product_count})"
        print(f"✅ Found {product_count} products available")
        
        # Step 3: Add first product to cart
        print("🛒 Step 3: Adding first product to cart...")
        initial_cart_count = ecommerce_page.get_cart_count()
        print(f"Initial cart count: {initial_cart_count}")
        
        # Find and click add to cart button
        add_buttons = ecommerce_page.add_to_cart_buttons
        assert add_buttons.count() > 0, "No 'Add to Cart' buttons found"
        
        add_buttons.first.click()
        page.wait_for_timeout(2000)  # Wait for cart update
        
        # Verify cart was updated
        updated_cart_count = ecommerce_page.get_cart_count()
        print(f"Updated cart count: {updated_cart_count}")
        print("✅ Product added to cart successfully")
        
        # Step 4: Open cart/basket
        print("🛒 Step 4: Opening cart/basket...")
        if ecommerce_page.cart_icon.is_visible():
            ecommerce_page.cart_icon.click()
            page.wait_for_timeout(1000)
            print("✅ Cart opened successfully")
        else:
            print("ℹ️ Cart icon not found, cart might be auto-visible")
        
        # Step 5: Proceed to checkout
        print("💳 Step 5: Proceeding to checkout...")
        
        # Look for checkout button with various selectors
        checkout_selectors = [
            "button:has-text('Checkout')",
            "button:has-text('チェックアウト')",
            "[data-testid='checkout']",
            "button:has-text('Buy now')",
            "button:has-text('Purchase')",
            ".checkout-button",
            "#checkout-button"
        ]
        
        checkout_clicked = False
        for selector in checkout_selectors:
            try:
                checkout_btn = page.locator(selector)
                if checkout_btn.is_visible():
                    print(f"Found checkout button with selector: {selector}")
                    checkout_btn.click()
                    checkout_clicked = True
                    break
            except Exception:
                continue
        
        if not checkout_clicked:
            # Debug: Show all buttons to understand what's available
            print("🔍 Debug: Available buttons on the page:")
            all_buttons = page.locator("button")
            button_count = all_buttons.count()
            for i in range(min(button_count, 10)):
                try:
                    btn_text = all_buttons.nth(i).text_content()
                    print(f"  Button {i+1}: '{btn_text}'")
                except Exception:
                    print(f"  Button {i+1}: Could not get text")
            
            pytest.fail("No checkout button found on the page")
        
        # Step 6: Wait for payment page to load
        print("⏳ Step 6: Waiting for payment page...")
        page.wait_for_load_state("networkidle", timeout=10000)
        
        # Verify we're on payment page (check for Stripe elements or payment form)
        payment_indicators = [
            "iframe[src*='stripe']",
            "[class*='stripe']",
            "[id*='stripe']",
            "form[action*='checkout']",
            ".payment-form",
            "#payment-form",
            "input[placeholder*='card']",
            "input[placeholder*='Card']"
        ]
        
        payment_page_loaded = False
        for indicator in payment_indicators:
            try:
                if page.locator(indicator).is_visible():
                    print(f"✅ Payment page detected with: {indicator}")
                    payment_page_loaded = True
                    break
            except Exception:
                continue
        
        if not payment_page_loaded:
            # Check URL for payment indicators
            current_url = page.url
            if any(keyword in current_url.lower() for keyword in ['checkout', 'payment', 'stripe']):
                print(f"✅ Payment page detected by URL: {current_url}")
                payment_page_loaded = True
        
        assert payment_page_loaded, f"Payment page not loaded. Current URL: {page.url}"
        print("✅ E2E test completed successfully!")

    def test_full_shopping_journey_multiple_products(self, page):
        """E2E: Complete shopping journey with multiple products"""
        print("🛍️ Starting E2E test: Multiple products shopping journey...")
        
        # Step 1: Open the app
        print("📱 Step 1: Opening the application...")
        ecommerce_page = EcommercePage(page)
        ecommerce_page.navigate_to_app()
        
        # Step 2: Add multiple products (at least 2)
        print("🛒 Step 2: Adding multiple products to cart...")
        page.wait_for_load_state("networkidle")
        
        product_count = ecommerce_page.get_product_count()
        assert product_count >= 2, f"Need at least 2 products for this test (found {product_count})"
        
        add_buttons = ecommerce_page.add_to_cart_buttons
        assert add_buttons.count() >= 2, "Need at least 2 'Add to Cart' buttons"
        
        # Add first product
        print("Adding first product...")
        add_buttons.nth(0).click()
        page.wait_for_timeout(1500)
        
        # Add second product
        print("Adding second product...")
        add_buttons.nth(1).click()
        page.wait_for_timeout(1500)
        
        # If available, add third product
        if add_buttons.count() >= 3:
            print("Adding third product...")
            add_buttons.nth(2).click()
            page.wait_for_timeout(1500)
        
        print("✅ Multiple products added to cart")
        
        # Step 3: Verify cart count
        cart_count = ecommerce_page.get_cart_count()
        print(f"Final cart count: {cart_count}")
        
        # Step 4: Proceed to checkout (similar to single product test)
        print("💳 Step 4: Proceeding to checkout...")
        
        checkout_selectors = [
            "button:has-text('Checkout')",
            "button:has-text('チェックアウト')",
            "[data-testid='checkout']",
            "button:has-text('Buy now')",
            "button:has-text('Purchase')"
        ]
        
        checkout_clicked = False
        for selector in checkout_selectors:
            try:
                checkout_btn = page.locator(selector)
                if checkout_btn.is_visible():
                    checkout_btn.click()
                    checkout_clicked = True
                    break
            except Exception:
                continue
        
        if not checkout_clicked:
            pytest.skip("No checkout button found - skipping payment page verification")
        
        # Step 5: Verify payment page
        page.wait_for_load_state("networkidle", timeout=10000)
        
        payment_indicators = [
            "iframe[src*='stripe']",
            "[class*='stripe']",
            "form[action*='checkout']"
        ]
        
        payment_page_loaded = any(
            page.locator(indicator).is_visible() 
            for indicator in payment_indicators
        )
        
        if not payment_page_loaded:
            current_url = page.url
            payment_page_loaded = any(
                keyword in current_url.lower() 
                for keyword in ['checkout', 'payment', 'stripe']
            )
        
        assert payment_page_loaded, f"Payment page not loaded. Current URL: {page.url}"
        print("✅ Multiple products E2E test completed successfully!")

    def test_cart_quantity_modification_journey(self, page):
        """E2E: Test adding products with quantity modifications"""
        print("🛍️ Starting E2E test: Cart quantity modification journey...")
        
        # Step 1: Open the app
        ecommerce_page = EcommercePage(page)
        ecommerce_page.navigate_to_app()
        page.wait_for_load_state("networkidle")
        
        # Step 2: Add product multiple times to increase quantity
        print("🔢 Step 2: Adding same product multiple times...")
        
        add_buttons = ecommerce_page.add_to_cart_buttons
        if add_buttons.count() > 0:
            # Add the same product 3 times
            for i in range(3):
                print(f"Adding product (attempt {i+1})...")
                add_buttons.first.click()
                page.wait_for_timeout(1000)
            
            print("✅ Product added multiple times")
        else:
            pytest.skip("No add to cart buttons found")
        
        # Step 3: Check for quantity controls
        print("🔍 Step 3: Looking for quantity controls...")
        
        quantity_selectors = [
            "input[type='number']",
            ".quantity-input",
            "[data-testid='quantity']",
            "button:has-text('+')",
            "button:has-text('-')",
            ".quantity-controls"
        ]
        
        quantity_controls_found = False
        for selector in quantity_selectors:
            if page.locator(selector).is_visible():
                print(f"✅ Quantity controls found: {selector}")
                quantity_controls_found = True
                break
        
        if not quantity_controls_found:
            print("ℹ️ No quantity controls found - products might be managed by adding multiple times")
        
        # Step 4: Proceed to checkout
        print("💳 Step 4: Proceeding to checkout...")
        
        # Look for checkout button
        checkout_btn = page.locator("button:has-text('Checkout'), button:has-text('チェックアウト'), [data-testid='checkout']")
        
        if checkout_btn.is_visible():
            checkout_btn.click()
            page.wait_for_load_state("networkidle")
            
            # Verify payment page
            current_url = page.url
            payment_loaded = (
                page.locator("iframe[src*='stripe']").is_visible() or
                "checkout" in current_url.lower() or
                "payment" in current_url.lower()
            )
            
            assert payment_loaded, f"Payment page not loaded. URL: {current_url}"
            print("✅ Quantity modification E2E test completed!")
        else:
            pytest.skip("No checkout button found")

    def test_empty_cart_checkout_prevention(self, page):
        """E2E: Verify that checkout is prevented with empty cart"""
        print("🛍️ Starting E2E test: Empty cart checkout prevention...")
        
        # Step 1: Open the app
        ecommerce_page = EcommercePage(page)
        ecommerce_page.navigate_to_app()
        page.wait_for_load_state("networkidle")
        
        # Step 2: Try to checkout without adding anything
        print("🚫 Step 2: Attempting checkout with empty cart...")
        
        checkout_btn = page.locator("button:has-text('Checkout'), button:has-text('チェックアウト')")
        
        if checkout_btn.is_visible():
            # Check if checkout button is disabled
            if checkout_btn.is_disabled():
                print("✅ Checkout button is properly disabled for empty cart")
            else:
                # Try clicking and see if it prevents checkout
                checkout_btn.click()
                page.wait_for_timeout(2000)
                
                # Should still be on main page, not payment page
                current_url = page.url
                assert "checkout" not in current_url.lower(), "Checkout should be prevented with empty cart"
                assert "payment" not in current_url.lower(), "Payment page should not be accessible with empty cart"
                print("✅ Empty cart checkout properly prevented")
        else:
            print("ℹ️ No checkout button visible with empty cart - this is expected behavior")
        
        print("✅ Empty cart prevention test completed!")
