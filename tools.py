from contextlib import contextmanager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import \
    staleness_of


#### from http://www.obeythetestinggoat.com/how-to-get-selenium-to-wait-for-page-load-after-a-click.html
class MySeleniumTest(SomeFunctionalTestClass):
    # assumes self.browser is a selenium webdriver

    @contextmanager
    def wait_for_page_load(self, timeout=30):
        old_page = self.browser.find_element_by_tag_name('html')
        yield
        WebDriverWait(self.browser, timeout).until(
            staleness_of(old_page)
        )

    def test_stuff(self):
        # example use
        with self.wait_for_page_load(timeout=10):
            self.browser.find_element_by_link_text('a link')
            # nice!
