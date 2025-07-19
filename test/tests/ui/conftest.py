import pytest
from pages.main import EcommercePage
from playwright.sync_api import Page


@pytest.fixture
def ecommerce_page(page: Page):
    """Create an EcommercePage instance without auto-navigation"""
    return EcommercePage(page)
