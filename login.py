from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json 

with open('config.json','r') as f:
    config = json.load(f)

enterprise_user = config['user_name']
user_password = config['user_password']
enterprise_id = config['enterprise_id']

def login_driver():

        # Start driver
        driver = webdriver.Chrome()
        # Wait 30 secs before raising exception of element not found
        driver.implicitly_wait(30)

        # Navigate driver to trunomi portal
        driver.get("http://trunomi.local/portal/login")
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