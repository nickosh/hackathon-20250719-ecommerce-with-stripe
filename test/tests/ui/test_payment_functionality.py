import pytest
from pages.main import EcommercePage
from playwright.sync_api import expect


class TestPaymentFunctionality:
    """Test suite for payment page and checkout functionality"""

    def test_checkout_button_navigation(self, page):
        """Test navigation to checkout/payment page"""
        print("💳 Testing checkout navigation...")
        ecommerce_page = EcommercePage(page)
        ecommerce_page.navigate_to_app()

        page.wait_for_load_state("networkidle")

        # Add a product first
        add_buttons = ecommerce_page.add_to_cart_buttons
        if add_buttons.count() == 0:
            pytest.skip("No products available to add to cart")

        add_buttons.first.click()
        page.wait_for_timeout(2000)

        # Look for checkout button
        checkout_buttons = page.locator(
            "button:has-text('Checkout'), button:has-text('チェックアウト'), "
            "[data-testid='checkout'], .checkout-btn, [class*='checkout']"
        )

        if checkout_buttons.count() > 0:
            print("✅ Checkout button found")
            checkout_buttons.first.click()
            page.wait_for_load_state("networkidle")

            # Check if we navigated to a checkout page
            current_url = page.url
            print(f"🌐 Navigation URL: {current_url}")

            if any(
                keyword in current_url.lower()
                for keyword in ["checkout", "payment", "stripe"]
            ):
                print("✅ Successfully navigated to checkout/payment page")
            else:
                print("ℹ️ Navigation completed but URL doesn't indicate checkout page")
        else:
            print("⚠️ No checkout button found")

    def test_stripe_integration_presence(self, page):
        """Test for Stripe payment integration elements"""
        print("🔌 Testing Stripe integration...")
        ecommerce_page = EcommercePage(page)
        ecommerce_page.navigate_to_app()

        page.wait_for_load_state("networkidle")

        # Add product and try to get to checkout
        add_buttons = ecommerce_page.add_to_cart_buttons
        if add_buttons.count() > 0:
            add_buttons.first.click()
            page.wait_for_timeout(2000)

        # Look for checkout button and click it
        checkout_buttons = page.locator(
            "button:has-text('Checkout'), button:has-text('チェックアウト'), "
            "[data-testid='checkout'], .checkout-btn"
        )

        if checkout_buttons.count() > 0:
            checkout_buttons.first.click()
            page.wait_for_timeout(3000)

            # Look for Stripe elements
            stripe_elements = page.locator(
                "[class*='stripe'], [id*='stripe'], iframe[src*='stripe'], "
                "[data-stripe], .StripeElement"
            )

            if stripe_elements.count() > 0:
                print("✅ Stripe payment elements detected")
            else:
                print("ℹ️ No obvious Stripe elements found on current page")
        else:
            pytest.skip("No checkout button available")

    def test_payment_form_elements(self, page):
        """Test for payment form elements"""
        print("📝 Testing payment form elements...")
        ecommerce_page = EcommercePage(page)
        ecommerce_page.navigate_to_app()

        page.wait_for_load_state("networkidle")

        # Add product and navigate to checkout
        add_buttons = ecommerce_page.add_to_cart_buttons
        if add_buttons.count() > 0:
            add_buttons.first.click()
            page.wait_for_timeout(2000)

            checkout_buttons = page.locator(
                "button:has-text('Checkout'), button:has-text('チェックアウト')"
            )

            if checkout_buttons.count() > 0:
                checkout_buttons.first.click()
                page.wait_for_timeout(3000)

                # Look for payment form elements
                payment_inputs = page.locator(
                    "input[type='text'], input[placeholder*='card'], input[placeholder*='カード'], "
                    "input[name*='card'], input[id*='card'], iframe"
                )

                if payment_inputs.count() > 0:
                    print(
                        f"✅ Found {payment_inputs.count()} potential payment form elements"
                    )
                else:
                    print("ℹ️ No payment form elements detected")
            else:
                pytest.skip("No checkout button available")
        else:
            pytest.skip("No products available")

    def test_checkout_with_empty_cart(self, page):
        """Test checkout behavior with empty cart"""
        print("🛒 Testing checkout with empty cart...")
        ecommerce_page = EcommercePage(page)
        ecommerce_page.navigate_to_app()

        page.wait_for_load_state("networkidle")

        # Ensure cart is empty (check initial state)
        cart_count = ecommerce_page.get_cart_count()
        print(f"🛒 Cart count: {cart_count}")

        # Look for checkout button when cart is empty
        checkout_buttons = page.locator(
            "button:has-text('Checkout'), button:has-text('チェックアウト')"
        )

        if checkout_buttons.count() > 0:
            # Check if checkout button is disabled for empty cart
            first_checkout = checkout_buttons.first
            is_disabled = first_checkout.is_disabled()

            if is_disabled:
                print("✅ Checkout button properly disabled for empty cart")
            else:
                print("ℹ️ Checkout button is enabled even with empty cart")
        else:
            print("ℹ️ No checkout button visible with empty cart (expected behavior)")

    def test_payment_security_indicators(self, page):
        """Test for payment security indicators"""
        print("🔒 Testing payment security indicators...")
        ecommerce_page = EcommercePage(page)
        ecommerce_page.navigate_to_app()

        page.wait_for_load_state("networkidle")

        # Add product and navigate to checkout
        add_buttons = ecommerce_page.add_to_cart_buttons
        if add_buttons.count() > 0:
            add_buttons.first.click()
            page.wait_for_timeout(2000)

            checkout_buttons = page.locator("button:has-text('Checkout')")
            if checkout_buttons.count() > 0:
                checkout_buttons.first.click()
                page.wait_for_timeout(3000)

                # Look for security indicators
                security_indicators = page.locator(
                    "[class*='secure'], [class*='ssl'], [class*='lock'], "
                    "text=/secure/i, text=/encrypted/i, text=/protected/i"
                )

                if security_indicators.count() > 0:
                    print("✅ Security indicators found")
                else:
                    print("ℹ️ No obvious security indicators found")

                # Check if page is HTTPS
                current_url = page.url
                if current_url.startswith("https://"):
                    print("✅ Page is served over HTTPS")
                else:
                    print("⚠️ Page is not served over HTTPS")
            else:
                pytest.skip("No checkout button available")
        else:
            pytest.skip("No products available")

    def test_order_summary_display(self, page):
        """Test order summary display on checkout page"""
        print("📋 Testing order summary display...")
        ecommerce_page = EcommercePage(page)
        ecommerce_page.navigate_to_app()

        page.wait_for_load_state("networkidle")

        # Add product and navigate to checkout
        add_buttons = ecommerce_page.add_to_cart_buttons
        if add_buttons.count() > 0:
            add_buttons.first.click()
            page.wait_for_timeout(2000)

            checkout_buttons = page.locator("button:has-text('Checkout')")
            if checkout_buttons.count() > 0:
                checkout_buttons.first.click()
                page.wait_for_timeout(3000)

                # Look for order summary elements
                summary_elements = page.locator(
                    "[class*='summary'], [class*='order'], [class*='total'], "
                    "text=/total/i, text=/subtotal/i, text=/¥/i"
                )

                if summary_elements.count() > 0:
                    print(f"✅ Found {summary_elements.count()} order summary elements")
                else:
                    print("ℹ️ No order summary elements detected")
            else:
                pytest.skip("No checkout button available")
        else:
            pytest.skip("No products available")

    def test_japan_region_restriction(self, page):
        """Test Japan region restriction mentioned in documentation"""
        print("🌏 Testing Japan region restriction...")
        ecommerce_page = EcommercePage(page)
        ecommerce_page.navigate_to_app()

        page.wait_for_load_state("networkidle")

        # Add product and try checkout
        add_buttons = ecommerce_page.add_to_cart_buttons
        if add_buttons.count() > 0:
            add_buttons.first.click()
            page.wait_for_timeout(2000)

            checkout_buttons = page.locator("button:has-text('Checkout')")
            if checkout_buttons.count() > 0:
                checkout_buttons.first.click()
                page.wait_for_timeout(3000)

                # Look for region/location related messages
                region_messages = page.locator(
                    "text=/japan/i, text=/region/i, text=/location/i, "
                    "text=/country/i, text=/地域/i, text=/日本/i"
                )

                if region_messages.count() > 0:
                    print("✅ Region-related messaging found")
                else:
                    print("ℹ️ No obvious region restriction messages found")
            else:
                pytest.skip("No checkout button available")
        else:
            pytest.skip("No products available")
