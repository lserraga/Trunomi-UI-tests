from selenium import webdriver
from selenium.webdriver.support.ui import Select
import unittest
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from random import randint, choice

with open('config.json', 'r') as f:
    config = json.load(f)

enterprise_id = config['enterprise_id']
crate_host = config['crate_host']
languages_exp = config['language_form']
erasures_exp = config['erasure_reasons_form']
host_addr = config['host_addr']

# with open('mockdata.json','r') as f:
#     data = json.load(f)

# enterprise = [aux for aux in data["Enterprises"] if aux["enterpriseId"] == enterprise_id][0]

# print(enterprise)

def send_sql_query(SQL_query):
    """
    Function to send SQL query
    """
    from crate import client

    connection = client.connect(crate_host)
    cursor = connection.cursor()
    cursor.execute(SQL_query)
    raw_data = cursor.fetchall()
    cursor.close()
    connection.close()

    return raw_data


def check_clickable(self, boxes, number):
    """
    Checks that there is the appropriate number of interactive elements and that they are enabled
    :param self: unitest case
    :param boxes: webelement
    :param number: int
    """
    self.assertEqual(len(boxes), number)
    for box in boxes:
        self.assertTrue(box.is_displayed and
                        box.is_enabled)


def check_form(self, form, expected):
    """
    Check that a form is correctly displayed
    :param self:  unitest case
    :param form: select class from selenium
    :param expected: array of options expected
    """
    options = form.options
    self.assertEqual(len(options), len(expected))
    for i in range(len(options)):
        self.assertEqual(options[i].text, expected[i])
        self.assertTrue(options[i].is_displayed() and
                        options[i].is_enabled())

    form.select_by_index(randint(0, len(options)-1))
    rand_num = randint(0, len(options)-1)
    form.select_by_index(rand_num)

    selection = form.all_selected_options
    # Assert that only one value can be asserted
    self.assertEqual(len(selection), 1)
    self.assertEqual(selection[0].text, expected[rand_num])


class DataTypes(unittest.TestCase):
    @classmethod
    def setUp(self):
        # Start driver
        self.driver = webdriver.Chrome()
        driver = self.driver
        driver.implicitly_wait(5)

        with open("session_key", 'r') as f:
            session_key = f.read()

        driver.get("{}/portal/login".format(host_addr))
        script = "sessionStorage.setItem('TRUNOMI_USE_TOKEN','{}')".format(session_key)
        driver.execute_script(script)
        driver.get("{}/portal/dashboard".format(host_addr))

    def test_datatypes_button(self):
        """ Testing that data types button redirects you to the proper page
        """
        driver = self.driver

        driver.find_element_by_link_text("Data Model").click()
        driver.find_element_by_link_text("Data Types").click()

        title_text = driver.find_element_by_css_selector('header.main-header span.navy-cap').text
        self.assertEqual(title_text.lower(), 'data type')
        self.assertEqual(driver.current_url, "{}/portal/data-model/data-type/view".format(host_addr))
        self.assertTrue("View Data Types for Enterprise" in driver.page_source)

    def test_raw_data_display(self):
        """ Test that all data types from the database are displayed
        """
        driver = self.driver

        driver.get("{}/portal/data-model/data-type/view".format(host_addr))

        # Loading data from crate
        # WHY DOES THE PLATFORM IMPORT DATA_TYPES FROM ENTERPRISE WITH ID=TRUNOMI?
        SQL_query = """SELECT id, name, collection, access_definition, rectify_definition, erasure_definition, \
        object_definition FROM dev.data_type WHERE enterprise_id = '{}' OR enterprise_id = 'TRUNOMI' ORDER BY \
        created_at DESC""".format(enterprise_id)
        raw_data = send_sql_query(SQL_query)

        # Loading displayed data
        rows = driver.find_elements_by_css_selector("div.react-bs-container-body tr")

        self.assertEqual(len(rows), len(raw_data), msg="Number of elements displayed different from the database")

        for i in range(len(rows)):
            columns = rows[i].find_elements_by_css_selector('td')
            driver.implicitly_wait(0.1)

            # Checking that all the values are displayed correctly
            for j in range(0, len(columns)):
                if j < 2:
                    self.assertTrue(columns[j].text in raw_data[i][j],
                                    msg="Found {}, should be {}".format(columns[j].text, raw_data[i][j]))

                elif j == 2:
                    # thumbs down
                    if (raw_data[i][j] == 'null'):
                        columns[j].find_element_by_css_selector("i.glyphicon.glyphicon-thumbs-down")
                    # thumbs up
                    else:
                        columns[j].find_element_by_css_selector("i.glyphicon.glyphicon-thumbs-up")

                elif j < 7:
                    # cross
                    if (raw_data[i][j] == 'null'):
                        columns[j].find_element_by_css_selector("i.glyphicon.glyphicon-remove")
                    # tick
                    else:
                        columns[j].find_element_by_css_selector("i.glyphicon.glyphicon-ok")
                else:
                    # button displayed and clickable
                    modify_button = columns[j].find_element_by_css_selector("button.btn.btn-warning")
                    self.assertTrue(modify_button.is_displayed())
                    self.assertTrue(modify_button.is_enabled())

    def test_add_button(self):
        """ Testing that add data type button redirects you to the proper page
        """
        driver = self.driver
        driver.get("{}/portal/data-model/data-type/view".format(host_addr))

        button = driver.find_element_by_css_selector("a.btn.btn-success")
        self.assertEqual("Add new Data Type ", button.text)
        button.click()

        driver.find_element_by_css_selector('button.btn.btn-primary')
        self.assertEqual(driver.current_url, "{}/portal/data-model/data-type/add".format(host_addr))
        self.assertTrue("Adds a New Data Type for Enterprise" in driver.page_source)

    def test_add_view(self):
        """ Testing the add view and all its elements
        """
        driver = self.driver
        driver.get("{}/portal/data-model/data-type/add".format(host_addr))

        forms_initial = driver.find_elements_by_css_selector("select.form-control")
        self.assertEqual(len(forms_initial), 1)

        check_form(self, Select(forms_initial[0]), languages_exp)

        check_clickable(self, driver.find_elements_by_css_selector('input.form-control'), 2)

        checkBoxes_initial = driver.find_elements_by_css_selector('div.btn.toggle.btn-md')

        exp_numberOf_textB = [3, 26, 47, 67, 88]
        exp_numberOf_checkB = [5, 6, 7, 8, 9]

        # Check that every click in check box displays the new textboxes/checkboxes
        for i in range(len(checkBoxes_initial)):
            checkBoxes_initial[i].click()
            check_clickable(self, driver.find_elements_by_css_selector('input.form-control'),
                            exp_numberOf_textB[i])
            check_clickable(self, driver.find_elements_by_css_selector('div.btn.toggle.btn-md'),
                            exp_numberOf_checkB[i])

        #Checking the new forms created
        forms = driver.find_elements_by_css_selector("select.form-control")
        self.assertEqual(len(forms), 5)
        for i in range(1, len(forms)):
            check_form(self, Select(forms[i]), erasures_exp)

        #Cancel and submit buttons
        submit_btn = driver.find_element_by_xpath("//button[contains(text(),'Submit')]")
        self.assertTrue(submit_btn.is_displayed() and submit_btn.is_enabled())
        cancel_btn = driver.find_element_by_xpath("//button[contains(text(),'Cancel')]")
        self.assertTrue(cancel_btn.is_displayed() and cancel_btn.is_enabled())

    def test_adding_dataType(self):
        """ Testing the add view and all its elements
        """
        driver = self.driver
        driver.get("{}/portal/data-model/data-type/add".format(host_addr))


        options = [choice([True, False]) for x in range(4)]
        checkBoxes = driver.find_elements_by_css_selector('div.btn.toggle.btn-md')
        for i in range(1, len(checkBoxes)):
            if options[i-1]:
                checkBoxes[i].click()

        text_input = driver.find_element_by_css_selector('input.form-control')
        test_name = "Test{}".format(randint(0, 3333))
        text_input.clear()
        text_input.send_keys(test_name)
        driver.find_element_by_xpath("//button[contains(text(),'Submit')]").click()

        #Checking pop up
        import time
        time.sleep(1)
        title = driver.find_element_by_id("contained-modal-title")
        self.assertEqual(title.text, 'Trunomi API - Add Data Type Successful')
        add_other_btn = driver.find_element_by_xpath("//button[contains(text(),'Add Another Data Type')]")
        close_btn = driver.find_element_by_xpath("//button[contains(text(),'Close')]")

        #Checking that close redirects to the view and check that the new data type is displayed
        close_btn.click()

        # time.sleep(2)
        # self.assertEqual("{}/portal/data-model/data-type/view".format(host_addr), driver.current_url)
        # # WebDriverWait(self.driver, 5) \
        # #     .until(expected_conditions.url_matches("{}/portal/data-model/data-type/view".format(host_addr)))
        #
        # self.assertTrue(test_name in driver.page_source)


    @classmethod
    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
