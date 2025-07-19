# tests/conftest.py
import pytest
from playwright.sync_api import BrowserContext, Page


@pytest.fixture(scope="function")
def browser_context_args(browser_context_args):
    """Configure browser context with reasonable timeouts"""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    """Create a page with configured timeouts"""
    page = context.new_page()

    # Set reasonable timeouts
    page.set_default_timeout(30000)  # 30 seconds
    page.set_default_navigation_timeout(30000)  # 30 seconds

    yield page
    page.close()
