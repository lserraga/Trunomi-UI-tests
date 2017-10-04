from selenium import webdriver
import unittest
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from test_data_types import send_sql_query

with open('config.json','r') as f:
    config = json.load(f)

enterprise_id = config['enterprise_id']
host_addr = config['host_addr']
menu_exp = config['main_menu']
subm1_exp = config['submenu_1']
subm2_exp = config['submenu_2']

class Dashboard(unittest.TestCase):

    # In a unittest.TestCase, this function is called every time before
    # running a test function
    @classmethod
    def setUp(self):
        # Start driver
        self.driver = webdriver.Chrome()
        driver = self.driver
        # Wait 30 secs before raising exception of element not found
        driver.implicitly_wait(5)

        with open("session_key",'r') as f:
            session_key = f.read()

        driver.get("{}/portal/login".format(host_addr))
        script = "sessionStorage.setItem('TRUNOMI_USE_TOKEN','{}')".format(session_key)
        driver.execute_script(script)
        # Navigate driver to trunomi portal
        driver.get("{}/portal/dashboard".format(host_addr))


    def test_stats(self):
        """Test that the stats numbers and charts are properly loaded """

        driver = self.driver

        stats_exp = 3 * ['']
        stats_exp[0] = send_sql_query("""SELECT COUNT(*) FROM dev.ledger WHERE \
        enterprise_id='{}'""".format(enterprise_id))[0][0]
        stats_exp[1] = send_sql_query("""SELECT COUNT(distinct customer_id) FROM \
        dev.enterprise_customer WHERE enterprise_id='{}'""".format(enterprise_id))[0][0]
        stats_exp[2] = send_sql_query("""SELECT COUNT(*) FROM(SELECT DISTINCT context_id, \
        payload['consent_definition_id'] FROM dev.ledger WHERE payload['consent_definition_id'] \
        >= 0 AND enterprise_id = '{}') As derivtable""".format(enterprise_id))[0][0]

        # Checking if the statistics are loaded propertly
        statistics = driver.find_elements_by_css_selector('div.col-md-4 h3.white')
        self.assertEqual(len(statistics), 3)
        for i in range(len(statistics)):
            self.assertEqual(str(stats_exp[i]), statistics[i].text,
                             msg='Stats not propertly loaded')

        charts = driver.find_elements_by_xpath("//*[contains(@id, 'chart-')]")
        self.assertTrue( 4 <= len(charts) <=8 )
        for chart in charts:
            self.assertTrue(chart.is_displayed())
            self.assertEqual(chart.text, '', msg=chart.text)


    def test_menus(self):
        """Test all elements of the left menu are properly displayed"""
        driver = self.driver

        def check_menu_displayed(menu, menu_exp):            
            for i in range (0,len(menu_exp)):
                menu_element = menu.find_element_by_link_text(menu_exp[i])
                self.assertTrue (menu_element.is_displayed())

        def check_menu_hidden(menu_exp):            
            for value in menu_exp:
                driver.implicitly_wait(0.1)
                assert len(driver.find_elements_by_link_text(value)) < 1

        menu = driver.find_element_by_class_name("sidebar-menu")
        check_menu_displayed(menu, menu_exp)

        # Checking that the menu toggle hides menu
        menu_toggle = driver.find_element_by_css_selector("a.sidebar-toggle")
        menu_toggle.click()
        check_menu_hidden(menu_exp)
        menu_toggle.click()

        # Submenus
        submenus = driver.find_elements_by_class_name("treeview")
        self.assertEqual (len(submenus), 2)

        # Checking the submenus properly open up 
        check_menu_hidden(subm1_exp)
        submenus[0].click()
        check_menu_displayed(submenus[0],subm1_exp)

        check_menu_hidden(subm2_exp)
        submenus[1].click()
        check_menu_displayed(submenus[1],subm2_exp)


    def test_redirect_logged(self):
        """Test that when having a session the portal redirects the
        user to the dashboard"""
        driver = self.driver
        driver.get("{}/portal".format(host_addr))
        WebDriverWait(self.driver, 5) \
            .until(expected_conditions.url_matches("{}/portal/dashboard".format(host_addr)))


        

    # The tearDown method will get called after every test method. This is 
    # a place to do all cleanup actions
    @classmethod
    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()              
