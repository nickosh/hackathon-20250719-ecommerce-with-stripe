from tests.constants import BASE_URL


class BasicPage:
    def __init__(self, page):
        self.page = page

    def __call__(self):
        return self.page

    def navigate(self):
        self.page.goto(BASE_URL)
