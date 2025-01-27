import random

from pycparser.ply.yacc import resultlimit
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import Select


class BusinessObjects:
    # Locators for various elements on the business creation part
    business_xpath = "//div[@id='selected-merchant']" #"//div[@class='merchant flex justify-between align-items-center']"
    add_business_option_xpath = "//span[normalize-space()='Add business']"
    business_creation_modal_message_xpath = "//div[@id='modals']//h2[1]"
    # form element
    error_message_on_business_modal_xpath = "//div[@class='error-div']"
    input_business_name_xpath = "//form/div[1]/div/input"
    category_xpath =   "//form[1]/div[1]/div[2]/div[1]/div[1]"
    category_list_xpath = "//div[@id='modals']//li[1]"
    description_input_xpath = "//textarea[@placeholder='tell us about your business']"
    next_button_xpath = "//button[normalize-space()='Next']"
    search_field_xpath = "//input[@type='text']"
    list_of_businesses = "//div[@class='dropdown-menu']//ul"
    first_result_on_list_xpath = "//div[@class='dropdown-menu']//ul[1]/li[1]"

    #page after the first
    back_button_xpath = "//button[normalize-space()='Back']"
    Country_selection_xpath = "//div[@class='data']/div[1]/div[1]"
    province_selection_xpath = "//div[@class='data']//div[2]/div[1]/div[1]"
    address_selection_xpath = "(//input[@autocomplete='off'])[1]"
    create_business_button_xpath = "//form[1]/div[2]/div[2]/button"




    def __init__(self, driver):
        # Initialize the driver
        self.driver = driver


    def locate_and_click_username_and_add_business_button(self, timeout=10):
        """
        Locate and click the username on the left navigation bar
        """
        try:
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=1,
                                 ignored_exceptions=[NoSuchElementException])
            username = wait.until(ec.element_to_be_clickable((By.XPATH, self.business_xpath)))
            username.click()
            add_business_button = wait.until(ec.element_to_be_clickable((By.XPATH, self.add_business_option_xpath)))
            add_business_button.click()
            business_modal_header = wait.until(ec.element_to_be_clickable((By.XPATH, self.business_creation_modal_message_xpath))).text
            return business_modal_header
        except TimeoutException:
            print(f"Sign-in button not found within {timeout} seconds")


    def locate_and_input_business_name(self, timeout=10):
        """
        Locate and input the name of the desired business
        """
        try:
            valid_chars = 'abcdefghijklmnopqrstuvwxyz'
            name_length = random.randint(6, 10)  # Use lowercase for variable names

            firstname = ''.join(random.choice(valid_chars) for _ in range(name_length))
            Company_name = f"{firstname} Company"
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=1,
                                 ignored_exceptions=[NoSuchElementException])
            # username = wait.until(ec.element_to_be_clickable((By.XPATH, self.business_xpath)))
            business_field_input = wait.until(ec.element_to_be_clickable((By.XPATH, self.input_business_name_xpath)))
            business_field_input.send_keys(Company_name)
            return  Company_name

        except TimeoutException:
            print(f"Sign-in button not found within {timeout} seconds")


    def select_a_category_from_all_the_options(self, category_number, timeout=10):
        try:
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=1,
                                 ignored_exceptions=[NoSuchElementException])
            category_element= wait.until(ec.element_to_be_clickable((By.XPATH, self.category_xpath)))
            category_element.click()
            time.sleep(3)
            self.driver.find_element(By.XPATH, f"//form[1]/div[1]/div[2]/div[1]/ul[1]/li[{category_number}]").click()

        except TimeoutException:
            print(f"No category was found within {timeout} seconds")


    def select_a_country_from_all_the_options(self, timeout=10):

        try:
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=1,
                                 ignored_exceptions=[NoSuchElementException])
            country_element= wait.until(ec.element_to_be_clickable((By.XPATH, self.Country_selection_xpath)))
            country_element.click()
            time.sleep(3)
            self.driver.find_element(By.XPATH, "//form[1]/div[1]/div[1]/div[1]/ul[1]/li[1]").click()

        except TimeoutException:
            print(f"No country was found within {timeout} seconds")


    def select_a_province_from_all_the_options(self, state_number, timeout=10):

        try:
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=1,
                                 ignored_exceptions=[NoSuchElementException])
            state_element = wait.until(ec.element_to_be_clickable((By.XPATH, self.province_selection_xpath)))
            state_element.click()
            time.sleep(3)
            self.driver.find_element(By.XPATH, f"//form[1]/div[1]/div[2]/div[1]/ul[1]/li[{state_number}]").click()

        except TimeoutException:
            print(f"No state was found within {timeout} seconds")


    def input_the_description_text(self, input_description, timeout=10):
        try:
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=1,
                                 ignored_exceptions=[NoSuchElementException])
            description_box = wait.until(ec.element_to_be_clickable((By.XPATH, self.description_input_xpath)))
            description_box.send_keys(input_description)

        except TimeoutException:
            print(f"No state was found within {timeout} seconds")


    def click_on_the_next_button(self, timeout=10):
        try:
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=1,
                                 ignored_exceptions=[NoSuchElementException])
            locate_next_button = wait.until(ec.presence_of_element_located((By.XPATH, self.next_button_xpath)))
            locate_next_button.click()

        except TimeoutException:
            print(f"The next button was not found within {timeout} seconds")


    def input_the_address_of_the_user(self, address, timeout=10):
        try:
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=1,
                                 ignored_exceptions=[NoSuchElementException])
            address_input_field = wait.until(ec.visibility_of_element_located((By.XPATH, self.address_selection_xpath)))
            address_input_field.send_keys(address)

        except TimeoutException:
            print(f"The address field was not found within {timeout} seconds")


    def click_on_the_create_business_button(self, timeout=10):
        try:
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=1, ignored_exceptions=[NoSuchElementException])
            create_business_button = wait.until(ec.presence_of_element_located((By.XPATH, self.create_business_button_xpath)))
            create_business_button.click()
        except TimeoutException:
            print(f"The create business button was not found within {timeout} seconds")


    def input_name_into_the_search_field(self, search_param, timeout=10):
        try:
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=1,  ignored_exceptions=[NoSuchElementException])
            username = wait.until(ec.element_to_be_clickable((By.XPATH, self.business_xpath)))
            username.click()
            locate_search_field = wait.until(ec.presence_of_element_located((By.XPATH, self.search_field_xpath)))
            locate_search_field.send_keys(search_param)

            # Get the name of the result and return it
            result_of_search = wait.until(ec.presence_of_element_located((By.XPATH, self.first_result_on_list_xpath))).text
            return result_of_search

        except TimeoutException:
            print(f"The search field was not found within {timeout} seconds")


    def select_a_business_and_check(self ,name_of_business ,timeout=10):
        try:
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=1,
                                 ignored_exceptions=[NoSuchElementException])
            username = wait.until(ec.element_to_be_clickable((By.XPATH, self.business_xpath)))
            username.click()
            businesses_options = Select(self.driver.find_element(By.XPATH, self.list_of_businesses))
            businesses_options.select_by_visible_text(name_of_business)

        except TimeoutException:
            print(f"Name was found within {timeout} seconds")



