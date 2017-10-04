from contextlib import contextmanager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import \
    staleness_of
from selenium import webdriver
import json 


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


with open('config.json','r') as f:
    config = json.load(f)

enterprise_user = config['user_name']
user_password = config['user_password']
host_addr = config['host_addr']

def login_driver():

        # Start driver
        driver = webdriver.Chrome()
        # Wait 30 secs before raising exception of element not found
        driver.implicitly_wait(30)

        # Navigate driver to trunomi portal
        driver.get("{}/portal/login".format(host_addr))
        assert "Enterprise Portal" in driver.title

        # Insert username
        user_box = driver.find_element_by_name("username")
        user_box.clear()
        user_box.send_keys(enterprise_user)

        # Insert password and submit
        pass_box = driver.find_element_by_name("password")
        pass_box.clear()
        pass_box.send_keys(user_password)
        driver.find_element_by_name("login-submit").click()

        return driver