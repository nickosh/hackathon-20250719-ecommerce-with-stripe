import re

from playwright.sync_api import expect

from models.basic_page import BasicPage


class MainPage(BasicPage):
    def __init__(self, page):
        super().__init__(page)
        self.page_title = re.compile("Playwright")
        self.get_started_link = page.get_by_role("link", name="Get started")

    def check_page_title(self):
        expect(self.page).to_have_title(self.page_title)
