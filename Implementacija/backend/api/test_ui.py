import shutil
from django.conf import settings
from django.test import LiveServerTestCase
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os
import io
import csv

# runs the tests with python manage.py test api.test_ui --settings=backend.ui_settings

class MySeleniumTests(LiveServerTestCase):
    """
    Author: Luka Mladenovic 0108-2021
    Author: Andrija Gajic 0033-2021
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome()
        cls.selenium.implicitly_wait(10)

        # Backup the database
        db_path = settings.DATABASES['default']['NAME']
        shutil.copyfile(db_path, f'{db_path}.backup')



    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()

        # Restore the database
        db_path = settings.DATABASES['default']['NAME']
        os.remove(db_path)
        shutil.move(f'{db_path}.backup', db_path)

        super().tearDownClass()

    def test_add_single_product(self):
        self.selenium.maximize_window()
        self.selenium.get(f'{self.live_server_url}/login')
        username_field = self.selenium.find_element(By.NAME, "username")
        username_field.send_keys("testreseller")
        password_field = self.selenium.find_element(By.NAME, "password")
        password_field.send_keys("123123123\n")
        time.sleep(1)

        self.selenium.get(f'{self.live_server_url}/dashboard-reseller')

        type_select = Select(self.selenium.find_element(By.NAME, 'type'))
        type_select.select_by_visible_text('iPhone 15')

        storage_select = Select(self.selenium.find_element(By.NAME, 'storage'))
        storage_select.select_by_visible_text('128GB')

        color_field = self.selenium.find_element(By.NAME, 'color')
        color_field.send_keys('black')

        price_field = self.selenium.find_element(By.NAME, 'price')
        price_field.send_keys('1100')

        add_product_form = self.selenium.find_element(By.CSS_SELECTOR, '#add-product .add-one-product form')
        add_product_form.submit()

        WebDriverWait(self.selenium, 10).until(EC.alert_is_present())

        alert = self.selenium.switch_to.alert
        alert_text = alert.text
        assert alert_text == "Product successfully added! Thank you!"
        alert.accept()
        time.sleep(2)
        # Assert that the user is redirected to the dashboard
        WebDriverWait(self.selenium, 10).until(EC.url_contains('/dashboard-reseller'))
        assert 'Logout' in self.selenium.page_source


class ApiInsertTests(LiveServerTestCase):
    """
    Author: Andrija Gajic 0033-2021
    """
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome()
        cls.selenium.implicitly_wait(10)

        db_path = settings.DATABASES['default']['NAME']
        shutil.copyfile(db_path, f'{db_path}.backup')



    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        
        db_path = settings.DATABASES['default']['NAME']
        os.remove(db_path)
        shutil.move(f'{db_path}.backup', db_path)
        super().tearDownClass()

    def test_add_single_product(self):
        self.selenium.maximize_window()
        self.selenium.get(f'{self.live_server_url}/shop')
        
        url = f'{self.live_server_url}/api/products/insert/api'
        data = {
            'api_key': 123123123,
            'type': 'iPhone 14',
            'price': 1000,
            'username': 'testreseller',
        }
        response = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
        time.sleep(1)
        
        self.selenium.find_element(By.XPATH, "//h6[contains(text(),'iPhone 14')]").click()
        time.sleep(1)
        
        assert 'TestReseller' in self.selenium.page_source

class RegisterCustomerTest(LiveServerTestCase):
    """
    Author: Luka Kaludjerovic 0041-2021
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome()
        cls.selenium.implicitly_wait(10)
        # Backup the database
        db_path = settings.DATABASES['default']['NAME']
        shutil.copyfile(db_path, f'{db_path}.backup')

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        # Restore the database
        db_path = settings.DATABASES['default']['NAME']
        os.remove(db_path)
        shutil.move(f'{db_path}.backup', db_path)
        super().tearDownClass()
    
    def test_register_customer(self):
        self.selenium.maximize_window()
        self.selenium.get(f'{self.live_server_url}/login')
        role_select = self.selenium.find_element(By.ID, 'customerradio')
        role_select.click()
        next_button = self.selenium.find_element(By.XPATH, "//input[@type='button' and @value='Next']")
        next_button.click()
        time.sleep(1)

        forename_field = self.selenium.find_element(By.NAME, 'forename')
        forename_field.send_keys('TestForename')
        surname_field = self.selenium.find_element(By.NAME, 'surname')
        surname_field.send_keys('TestSurname')
        email_field = self.selenium.find_element(By.NAME, 'email')
        email_field.send_keys('test@test.com')
        username_field = self.selenium.find_element(By.NAME, 'username')
        username_field.send_keys('TestCustomer')
        phonenumber_field = self.selenium.find_element(By.NAME, 'phonenumber')
        phonenumber_field.send_keys('123456789')
        password1_field = self.selenium.find_element(By.NAME, 'password1')
        password1_field.send_keys('123123123')
        password2_field = self.selenium.find_element(By.NAME, 'password2')
        password2_field.send_keys('123123123')
        register_button = self.selenium.find_element(By.XPATH, "//input[@type='submit' and @value='Register']")
        register_button.click()
        
        WebDriverWait(self.selenium, 10).until(EC.alert_is_present())
        alert = self.selenium.switch_to.alert
        alert_text = alert.text
        assert alert_text == "Account successfully created! Welcome!"
        alert.accept()
        time.sleep(1)

        dashboard_label = WebDriverWait(self.selenium, 10).until(EC.presence_of_element_located((By.XPATH, "//*[text()='Dashboard']")))
        assert dashboard_label is not None, 'An error ocured'
        time.sleep(1)
class VukanSeleniumTests(LiveServerTestCase):
    """
    Author: Vukan Terzic 2021-0334
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome()
        cls.selenium.implicitly_wait(10)

        db_path = settings.DATABASES['default']['NAME']
        shutil.copyfile(db_path, f'{db_path}.backup')

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        db_path = settings.DATABASES['default']['NAME']
        os.remove(db_path)
        shutil.move(f'{db_path}.backup', db_path)

        super().tearDownClass()

    def test_seirialized_product_insert(self):
        self.selenium.maximize_window()
        self.selenium.get(f'{self.live_server_url}/login')
        username_field = self.selenium.find_element(By.NAME, "username")
        username_field.send_keys("testreseller")
        password_field = self.selenium.find_element(By.NAME, "password")
        password_field.send_keys("123123123\n")
        time.sleep(1)

        self.selenium.get(f'{self.live_server_url}/dashboard-reseller')

        data = {
            "supported_item_id": [10, 11],
            "price": [1000, 2000]
        }
        csv_file = io.StringIO()
        writer = csv.writer(csv_file)
        writer.writerow(data.keys())
        writer.writerows(zip(*data.values()))
        csv_file.seek(0)
        
        #file_data = SimpleUploadedFile("temp_test.csv", csv_file.getvalue().encode(), content_type='text/csv')

        with open("./temp_test.csv", "w") as temp_file:
            temp_file.write(csv_file.getvalue())

        add_product_form = self.selenium.find_element(By.ID, 'fileInput')
        add_product_form.send_keys(os.getcwd() + "/temp_test.csv")

        add_button = self.selenium.find_element(By.XPATH, "//input[@type='submit' and @value='Add products']")
        add_button.click()

        WebDriverWait(self.selenium, 10).until(EC.alert_is_present())

        alert = self.selenium.switch_to.alert
        alert_text = alert.text
        assert alert_text == "Product successfully added! Thank you!"
        alert.accept()

        WebDriverWait(self.selenium, 10).until(EC.url_contains('/dashboard-reseller'))
        self.selenium.refresh()
        
        time.sleep(1)
        self.selenium.refresh()
        your_phones = self.selenium.find_element(By.ID, 'smartphones')
        paragraph_elements = your_phones.find_elements(By.TAG_NAME, "p")
        
        count = 0
        for element in paragraph_elements:
            if "1000" in element.text or "2000" in element.text:
                count+=1
        self.selenium.refresh()
        assert count >= 2

    def test_logout(self):
        self.selenium.maximize_window()
        self.selenium.get(f'{self.live_server_url}/login')
        username_field = self.selenium.find_element(By.NAME, "username")
        username_field.send_keys("testreseller")
        password_field = self.selenium.find_element(By.NAME, "password")
        password_field.send_keys("123123123\n")
        time.sleep(1)

        logout_a = self.selenium.find_element(By.XPATH, "//a[@class='nav-link' and text()='Logout']")
        logout_a.click()

        WebDriverWait(self.selenium, 10).until(EC.alert_is_present())

        alert = self.selenium.switch_to.alert
        alert.accept()

        time.sleep(1)
        assert "Login" in self.selenium.page_source
