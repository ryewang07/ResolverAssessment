import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

HOME_URL = "file:///" + os.path.abspath("QE-index.html").replace("\\", "/")


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(5)
        cls.wait = WebDriverWait(cls.driver, 15)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def open_home(self):
        self.driver.get(HOME_URL)

    def get_container(self, container_id):
        return self.driver.find_element(By.ID, container_id)


class UITests(BaseTest):

    def test_1(self):
        """Test #1: Login fields in test-1-div
            - Navigate to the home page
            - Assert that both the email address and password inputs are present as well as the login button
            - Enter in an email address and password combination into the respective fields
        """
        self.open_home()
        container = self.get_container("test-1-div")

        email = container.find_element(By.ID, "inputEmail")
        password = container.find_element(By.ID, "inputPassword")
        button = container.find_element(By.CSS_SELECTOR, "button.btn.btn-lg.btn-primary")

        self.assertTrue(email.is_displayed())
        self.assertTrue(password.is_displayed())
        self.assertTrue(button.is_displayed())

        email.send_keys("test@example.com")
        password.send_keys("passwordtest")

    def test_2(self):
        """Test #2: List item content and badge in test-2-div
            - Navigate to the home page
            - In the test 2 div, assert that there are three values in the listgroup
            - Assert that the second list item's value is set to "List Item 2"
            - Assert that the second list item's badge value is 6
        """
        self.open_home()
        container = self.get_container("test-2-div")
        items = container.find_elements(By.CSS_SELECTOR, "ul.list-group > li.list-group-item")

        self.assertEqual(len(items), 3)

        item2 = items[1]
        badge = item2.find_element(By.CSS_SELECTOR, "span.badge.badge-pill.badge-primary")

        self.assertIn("List Item 2", item2.text.strip())
        self.assertEqual(badge.text, "6")

    def test_3(self):
        """Test #3: Dropdown menu behavior in test-3-div
            - Navigate to the home page
            - In the test 3 div, assert that "Option 1" is the default selected value
            - Select "Option 3" from the select list
        """
        self.open_home()
        container = self.get_container("test-3-div")
        button = container.find_element(By.ID, "dropdownMenuButton")
        menu = container.find_element(By.CSS_SELECTOR, "div.dropdown-menu")

        self.assertEqual(button.text.strip(), "Option 1")

        button.click()
        menu.find_element(By.XPATH, ".//a[text()='Option 3']").click()

        self.assertEqual(button.text.strip(), "Option 3")

    def test_4(self):
        """Test #4: Button enable/disable state in test-4-div
            - Navigate to the home page
            - In the test 4 div, assert that the first button is enabled and that the second button is disabled
        """
        self.open_home()
        container = self.get_container("test-4-div")
        buttons = container.find_elements(By.CSS_SELECTOR, "button.btn.btn-lg")

        self.assertTrue(buttons[0].is_enabled())
        self.assertFalse(buttons[1].is_enabled())

    def test_5(self):
        """Test #5: Delayed button + alert behavior in test-5-div
            - Navigate to the home page
            - In the test 5 div, wait for a button to be displayed (note: the delay is random) and then click it
            - Once you've clicked the button, assert that a success message is displayed
            - Assert that the button is now disabled
        """
        self.open_home()
        container = self.get_container("test-5-div")

        button = self.wait.until(
            expected_conditions.visibility_of_element_located((By.ID, "test5-button"))
        )
        placeholder = container.find_element(By.ID, "test5-placeholder")
        self.assertFalse(placeholder.is_displayed())

        button.click()
        alert = container.find_element(By.ID, "test5-alert")

        self.assertTrue(alert.is_displayed())
        self.assertFalse(button.is_enabled())

    def test_6(self):
        """Test #6: Table cell content in test-6-div
            - Navigate to the home page
            - Write a method that allows you to find the value of any cell on the grid
            - Use the method to find the value of the cell at coordinates 2, 2 (staring at 0 in the top left corner)
            - Assert that the value of the cell is "Ventosanzap"
        """
        self.open_home()
        container = self.get_container("test-6-div")
        table = container.find_element(By.CSS_SELECTOR, "table.table-bordered.table-dark")
        tbody = table.find_element(By.TAG_NAME, "tbody")

        def get_cell(row, col):
            rows = tbody.find_elements(By.TAG_NAME, "tr")
            assert 0<= row < len(rows)
            cols = rows[row].find_elements(By.TAG_NAME, "td")
            assert 0<= col < len(cols)
           
            return cols[col].text

        self.assertEqual(get_cell(2, 2), "Ventosanzap")


if __name__ == "__main__":
    unittest.main()
