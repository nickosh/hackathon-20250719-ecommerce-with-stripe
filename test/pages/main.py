import re

from models.basic_page import BasicPage
from playwright.sync_api import expect


class EcommercePage(BasicPage):
    def __init__(self, page):
        super().__init__(page)

        # Requirements page elements
        self.start_qa_button = page.locator(
            "button", has_text="Let's start the QA Hackathon"
        )
        self.any_button = page.locator("button")

        # E-commerce page elements
        self.page_title = page.locator("h1")
        self.product_cards = page.locator(
            "[data-testid='product-card'], .product-card, .grid > div, .product"
        )
        self.product_titles = page.locator("h3, .product-title, h2")
        self.product_prices = page.locator("[class*='price'], .price, .cost")
        self.add_to_cart_buttons = page.locator(
            "button:has-text('Add to Cart'), button:has-text('カートに追加'), button:has-text('Add'), .add-to-cart"
        )
        self.cart_icon = page.locator(
            "[data-testid='cart-icon'], .cart-icon, [aria-label*='cart'], .cart"
        )
        self.cart_counter = page.locator("[data-testid='cart-count'], .cart-count, .cart-quantity")

        # Cart/Basket elements
        self.quantity_inputs = page.locator("input[type='number'], .quantity-input")
        self.quantity_plus_buttons = page.locator("button:has-text('+'), .quantity-plus")
        self.quantity_minus_buttons = page.locator("button:has-text('-'), .quantity-minus")
        self.cart_items = page.locator(".cart-item, [data-testid='cart-item']")
        self.remove_item_buttons = page.locator("button:has-text('Remove'), .remove-item")

        # Checkout elements
        self.checkout_button = page.locator(
            "button:has-text('Checkout'), button:has-text('チェックアウト'), [data-testid='checkout'], button:has-text('Buy now'), button:has-text('Purchase')"
        )
        self.stripe_elements = page.locator(
            "[class*='stripe'], [id*='stripe'], iframe[src*='stripe']"
        )
        self.payment_form = page.locator("form[action*='checkout'], .payment-form, #payment-form")

    def navigate_to_app(self):
        """Navigate to the app and handle requirements page if present"""
        # First try the requirements page
        self.page.goto("https://ecommerce-with-stripe-six.vercel.app/")
        self.page.wait_for_load_state("networkidle")

        # Check if we're on the requirements page
        try:
            if self.start_qa_button.is_visible():
                print(
                    "📋 Requirements page detected, clicking 'Let's start the QA Hackathon' button..."
                )
                self.start_qa_button.click()
                # Wait for any content changes
                self.page.wait_for_timeout(2000)
                print("✅ Successfully clicked the requirements button!")
            else:
                print("✅ No requirements page found, navigating to main app...")
                self.navigate()  # Fall back to main URL
        except Exception:
            print("✅ No requirements page found, navigating to main app...")
            self.navigate()  # Fall back to main URL

        return self

    def navigate_to_main(self):
        """Navigate directly to the main page (alias for navigate_to_app)"""
        return self.navigate_to_app()

    def is_on_requirements_page(self):
        """Check if we're currently on the requirements page"""
        try:
            return self.start_qa_button.is_visible()
        except Exception:
            return False

    def debug_page_content(self):
        """Debug method to see what's on the page"""
        print("🔍 Debugging page content...")

        # Check page title
        try:
            title = self.page.title()
            print(f"📄 Page title: {title}")
        except Exception as e:
            print(f"❌ Could not get page title: {e}")

        # Check for buttons
        try:
            button_count = self.any_button.count()
            print(f"🔘 Found {button_count} buttons on the page")

            if button_count > 0:
                for i in range(min(button_count, 5)):  # Show first 5 buttons
                    try:
                        button_text = self.any_button.nth(i).text_content()
                        print(f"  Button {i + 1}: '{button_text}'")
                    except Exception:
                        print(f"  Button {i + 1}: Could not get text")
        except Exception as e:
            print(f"❌ Could not analyze buttons: {e}")

        # Check URL
        try:
            current_url = self.page.url
            print(f"🌐 Current URL: {current_url}")
        except Exception as e:
            print(f"❌ Could not get URL: {e}")

        return self

    def click_start_qa_button(self):
        """Click the 'Let's start the QA Hackathon' button"""
        try:
            if self.start_qa_button.is_visible():
                self.start_qa_button.click()
                self.page.wait_for_load_state("networkidle")
        except Exception:
            pass
        return self

    def get_page_title(self):
        """Get the main page title"""
        return self.page_title.text_content()

    def get_product_count(self):
        """Get the number of products displayed"""
        return self.product_cards.count()

    def get_first_product_title(self):
        """Get the title of the first product"""
        return self.product_titles.first.text_content()

    def get_first_product_price(self):
        """Get the price of the first product"""
        return self.product_prices.first.text_content()

    def add_first_product_to_cart(self):
        """Add the first product to cart"""
        self.add_to_cart_buttons.first.click()
        return self

    def get_cart_count(self):
        """Get the cart item count"""
        try:
            return self.cart_counter.text_content()
        except Exception:
            return "0"

    def click_cart_icon(self):
        """Click on the cart icon"""
        self.cart_icon.click()
        return self

    def click_checkout_button(self):
        """Click the checkout button"""
        try:
            if self.checkout_button.is_visible():
                self.checkout_button.click()
                self.page.wait_for_load_state("networkidle")
        except Exception:
            pass
        return self

    def is_checkout_button_visible(self):
        """Check if checkout button is visible"""
        try:
            return self.checkout_button.is_visible()
        except Exception:
            return False

    def is_checkout_button_enabled(self):
        """Check if checkout button is enabled"""
        try:
            return not self.checkout_button.is_disabled()
        except Exception:
            return False

    def is_payment_page_loaded(self):
        """Check if we're on a payment page"""
        try:
            # Check for Stripe elements
            if self.stripe_elements.is_visible():
                return True
            
            # Check for payment form
            if self.payment_form.is_visible():
                return True
            
            # Check URL for payment indicators
            current_url = self.page.url
            payment_keywords = ['checkout', 'payment', 'stripe', 'buy']
            return any(keyword in current_url.lower() for keyword in payment_keywords)
        except Exception:
            return False

    def add_product_to_cart_by_index(self, index=0):
        """Add a specific product to cart by index"""
        try:
            if self.add_to_cart_buttons.count() > index:
                self.add_to_cart_buttons.nth(index).click()
                self.page.wait_for_timeout(1000)
                return True
        except Exception:
            pass
        return False

    def add_multiple_products_to_cart(self, count=2):
        """Add multiple different products to cart"""
        added_count = 0
        max_products = min(count, self.add_to_cart_buttons.count())
        
        for i in range(max_products):
            if self.add_product_to_cart_by_index(i):
                added_count += 1
                print(f"Added product {i+1} to cart")
        
        return added_count

    def increase_product_quantity(self, product_index=0):
        """Increase quantity of a product (if quantity controls exist)"""
        try:
            if self.quantity_plus_buttons.count() > product_index:
                self.quantity_plus_buttons.nth(product_index).click()
                self.page.wait_for_timeout(500)
                return True
        except Exception:
            pass
        return False

    def get_cart_items_count(self):
        """Get the number of items in cart"""
        try:
            return self.cart_items.count()
        except Exception:
            return 0

    def debug_checkout_elements(self):
        """Debug method to see checkout-related elements"""
        print("🔍 Debugging checkout elements...")
        
        # Check for checkout buttons
        all_buttons = self.page.locator("button")
        button_count = all_buttons.count()
        print(f"Found {button_count} total buttons:")
        
        for i in range(min(button_count, 10)):
            try:
                btn_text = all_buttons.nth(i).text_content()
                is_visible = all_buttons.nth(i).is_visible()
                is_enabled = not all_buttons.nth(i).is_disabled()
                print(f"  Button {i+1}: '{btn_text}' (visible: {is_visible}, enabled: {is_enabled})")
            except Exception:
                print(f"  Button {i+1}: Could not analyze")
        
        # Check current URL
        print(f"Current URL: {self.page.url}")
        
        return self

    def check_page_loaded(self):
        """Verify the page has loaded properly"""
        expect(self.page).to_have_url(re.compile("ecommerce-with-stripe"))
        expect(self.product_cards.first).to_be_visible()
