from selenium import webdriver
import unittest
import time
import json 

with open('config.json','r') as f:
    config = json.load(f)

enterprise_user = config['user_name']
user_password = config['user_password']
enterprise_id = config['enterprise_id']

class LogIn(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)

    def test_redirect(self):
        """Test that user is redirected to login page if out of session"""

        driver = self.driver
        driver.get("http://trunomi.local/portal")
        time.sleep(1)
        assert driver.current_url == "http://trunomi.local/portal/login"


    def test_login(self):
        """Test logging in. Stores the session key so other tests can use 
        it
        """

        driver = self.driver
        # Navigate driver to trunomi portal
        driver.get("http://trunomi.local/portal/login")
        self.assertTrue("Enterprise Portal" in driver.title)

        # Insert username
        user_box = driver.find_element_by_name("username")
        user_box.clear()
        user_box.send_keys(enterprise_user)

        # Insert password and submit
        pass_box = driver.find_element_by_name("password")
        pass_box.clear()
        pass_box.send_keys(user_password)
        driver.find_element_by_name("login-submit").click()

        # Asserint that the log-in was proper
        welcome_text = driver.find_element_by_css_selector('header.main-header span.navy-cap').text
        self.assertEqual("welcome {}".format(enterprise_user), welcome_text.lower())
        self.assertEqual(driver.current_url, "http://trunomi.local/portal/dashboard")

        session_key = driver.execute_script("return sessionStorage.getItem('TRUNOMI_USE_TOKEN')")
        self.assertTrue(session_key.startswith('Bearer '))
        with open("session_key",'w') as f:
            f.write(session_key)

    @classmethod
    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()              
