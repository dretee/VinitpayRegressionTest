import random

from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class LoginObjects:
    # Locators for various elements on the business creation part
    business_xpath = "//div[@id='selected-merchant']"
    add_business_option_xpath = "//span[normalize-space()='Add business']"
    business_creation_modal_message_xpath = "//div[@id='modals']//h2[1]"
    # form element
    error_message_on_business_modal_xpath = "//div[@class='error-div']"
    input_business_name_xpath = "//form/div[1]/div/input"
    category_xpath = "//div[@class='data']//div[@class='dropdown-selected']"
    description_input_xpath = "//textarea[@placeholder='tell us about your business']"
    next_button_xpath = "//button[normalize-space()='Next']"

    #page after the first
    back_button_xpath = "//button[normalize-space()='Back']"
    Country_selection_xpath = "(//div[@id='dropdown'])[3]"
    province_selection_xpath = "//div[@class='data']//div[2]/div[1]/div[1]"
    address_selection_xpath = "(//input[@autocomplete='off'])[1]"
    create_business_button_xpath = "//form[1]/div[2]/div[2]/button[1]"




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
            add_business_button = wait.until(ec.element_to_be_clickable((By.XPATH, self.add_business_option_xpath)))
            username.click()
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
            Company_name = f"{firstname} + & Sons"
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=1,
                                 ignored_exceptions=[NoSuchElementException])
            username = wait.until(ec.element_to_be_clickable((By.XPATH, self.business_xpath)))
            business_field_input = wait.until(ec.element_to_be_clickable((By.XPATH, self.input_business_name_xpath)))
            business_field_input.send_keys(Company_name)

        except TimeoutException:
            print(f"Sign-in button not found within {timeout} seconds")



