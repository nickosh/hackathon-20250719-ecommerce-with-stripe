from playwright.sync_api import expect

from pages.main import MainPage


def test_has_title(test_page: MainPage):
    test_page.check_page_title()


def test_get_started_link(test_page: MainPage):
    # Click the get started link.
    test_page().get_by_role("link", name="Get started").click()

    # Expects page to have a heading with the name of Installation.
    expect(test_page.page.get_by_role("heading", name="Installation")).to_be_visible()
