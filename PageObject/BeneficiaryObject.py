from selenium import webdriver
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException,NoSuchElementException


class BeneficiaryObjects:
    Beneficiary_navigation_xpath = "//a[normalize-space()='Beneficiaries']"
    New_Beneficiary_xpath = "//button[normalize-space()='New Beneficiary']"

    # Deactivation locators
    Deactivate_ana_activate_beneficiary_button_xpath = "//tbody/tr[1]/td[5]/button"
    Activation_deactivation_button_text_Xpath = ""
    Beneficiary_status_xpath = "//tbody/tr[1]/td[4]/span"

    # The new beneficiary number is 1-3; 1 is for automobile, 2 is for students, and 3 is for others
    New_other_Beneficiary_option_xpath = "//section[@id='actions']/a[3]"
    New_Automobile_Beneficiary_option_xpath = "//section[@id='actions']/a[1]"
    New_Students_Beneficiary_option_xpath = "//section[@id='actions']/a[2]"
    Proceed_button_other_xpath = "//button[@type='submit']"
    name_of_beneficiary_xpath = "//tbody/tr[1]/td[3]"

    # other beneficiary creation
    Other_beneficiary_phone_number_xpath = "//div[@id='left']//div[1]//input[1]"
    Other_beneficiary_Firstname_xpath = "//div[@id='left']//div[2]//input[1]"
    Other_beneficiary_Lastname_xpath = "//div[@id='left']//div[3]//input[1]"
    Other_beneficiary_email_xpath = "//input[@type='email']"

    # Automobile beneficiary creation
    Automobile_beneficiary_Reg_number_xpath = "(//input[@type='text'])[1]"
    automobile_beneficiary_enter_vin_xpath = "(//input[@type='text'])[2]"
    Next_button_xpath = "//button[normalize-space()='Next']"

    # student beneficiary creation: Currently schools registration is down
    student_number_xpath = "(//input[@type='text'])[1]"
    student_firstname_xpath = "(//input[@type='text'])[2]"
    student_lastname_xpath = "(//input[@type='text'])[3]"
    student_email_xpath = "//input[@type='email']"
    student_phone_number_xpath = "(//input[@type='text'])[4]"
    student_course_xpath = "(//input[@type='text'])[5]"

    # alert locators on the beneficiary page
    alert_xpath = "//div[@class='Vue-Toastification__container top-right']//div[@role='alert']"

    def __init__(self, driver):
        # Initialize the driver
        self.driver = driver
        wait = WebDriverWait(self.driver, timeout=10, poll_frequency=1, ignored_exceptions=[NoSuchElementException])

    def click_on_the_Beneficiary_option(self, timeout=10):
        try:
            wait = WebDriverWait(self.driver, timeout=10, poll_frequency= 1, ignored_exceptions= [NoSuchElementException])
            element = wait.until(ec.presence_of_element_located((By.XPATH, self.Beneficiary_navigation_xpath)))
            element.click()
        except TimeoutException:
            print(f"Name input field not found within {timeout} seconds")

    def click_on_the_new_beneficiary_button(self, timeout=10):
        try:
            wait = WebDriverWait(self.driver, timeout=10, poll_frequency= 1, ignored_exceptions=[NoSuchElementException])
            element = wait.until(ec.presence_of_element_located((By.XPATH, self.New_Beneficiary_xpath)))
            element.click()
        except TimeoutException:
            print(f"Name input field not found within {timeout} seconds")

    def click_on_the_proceed_button(self, timeout=10):
        try:
            wait = WebDriverWait(self.driver, timeout=10, poll_frequency= 1, ignored_exceptions=[NoSuchElementException])
            element = wait.until(ec.presence_of_element_located((By.XPATH, self.Proceed_button_other_xpath)))
            element.click()
        except TimeoutException:
            print(f"Proceed button input field not found within {timeout} seconds")

    """
    This are the actions for the other beneficiary creation. 
    It contains all the actions from navigations to the input of details on the UI and the proceeding function
    """

    def click_on_the_other_beneficiary_option(self, timeout=10):
        try:
            wait = WebDriverWait(self.driver, timeout=10, poll_frequency=1, ignored_exceptions=[NoSuchElementException])
            element = wait.until(ec.presence_of_element_located((By.XPATH, self.New_other_Beneficiary_option_xpath)))
            element.click()
        except TimeoutException:
            print(f"Other beneficiary button input field not found within {timeout} seconds")

    def input_phone_number(self, number,timeout=10):
        try:
            wait = WebDriverWait(self.driver, timeout=10, poll_frequency= 1, ignored_exceptions=[NoSuchElementException])
            element = wait.until(ec.presence_of_element_located((By.XPATH, self.Other_beneficiary_phone_number_xpath)))
            element.clear()
            element.send_keys(number)
        except TimeoutException:
            print(f"Phone number input field not found within {timeout} seconds")

    def input_first_name(self, First_name, timeout=10):
        try:
            wait = WebDriverWait(self.driver, timeout=10, poll_frequency= 1, ignored_exceptions=[NoSuchElementException])
            element = wait.until(ec.presence_of_element_located((By.XPATH, self.Other_beneficiary_Firstname_xpath)))
            element.clear()
            element.send_keys(First_name)
        except TimeoutException:
            print(f"First name input field not found within {timeout} seconds")

    def input_last_name(self, lastname, timeout= 10):
        try:
            wait = WebDriverWait(self.driver, timeout=10, poll_frequency=1, ignored_exceptions=[NoSuchElementException])
            element = wait.until(ec.presence_of_element_located((By.XPATH, self.Other_beneficiary_Lastname_xpath)))
            element.clear()
            element.send_keys(lastname)
        except TimeoutException:
            print(f"Last name input field not found within {timeout} seconds")

    def input_email(self, email, timeout=10):
        try:
            wait = WebDriverWait(self.driver, timeout=10, poll_frequency=1, ignored_exceptions=[NoSuchElementException])
            element = wait.until(ec.presence_of_element_located((By.XPATH, self.Other_beneficiary_email_xpath)))
            element.clear()
            element.send_keys(email)
        except TimeoutException:
            print(f"Email input field not found within {timeout} seconds")

    """
    This are the actions for the automobile beneficiary creation. 
    It contains all the actions from navigations to the input of details on the UI and the proceeding function
    """

    def click_on_the_automobile_beneficiary_option(self, timeout=10):
        try:
            wait = WebDriverWait(self.driver, timeout=10, poll_frequency=1, ignored_exceptions=[NoSuchElementException])
            element = wait.until(ec.visibility_of_element_located((By.XPATH, self.New_Automobile_Beneficiary_option_xpath)))
            element.click()
        except TimeoutException:
            print(f"Name input field not found within {timeout} seconds")

    def get_the_text_for_the_alert_to_the_user(self, timeout=10):
        try:
            wait = WebDriverWait(self.driver, timeout=10, poll_frequency=1, ignored_exceptions=[NoSuchElementException])
            element = wait.until(ec.presence_of_element_located((By.XPATH, self.alert_xpath)))
            time.sleep(4)
            name_of_beneficiary_on_table = wait.until(ec.presence_of_element_located((By.XPATH, self.name_of_beneficiary_xpath)))
            return element.text, name_of_beneficiary_on_table.text
        except TimeoutException:
            print(f"Name input field not found within {timeout} seconds")

    def input_reg_number(self, reg_number, timeout=10):
        try:
            wait = WebDriverWait(self.driver, timeout=10, poll_frequency=1, ignored_exceptions=[NoSuchElementException])
            element = wait.until(ec.visibility_of_element_located((By.XPATH, self.New_Beneficiary_option_xpath)))
            element.clear()
            element.send_keys(reg_number)
        except TimeoutException:
            print(f"Name input field not found within {timeout} seconds")

    def input_vin_number(self, vin_number, timeout=10):
        try:
            wait = WebDriverWait(self.driver, timeout=10, poll_frequency=1, ignored_exceptions=[NoSuchElementException])
            element = wait.until(ec.visibility_of_element_located((By.XPATH, self.New_Beneficiary_option_xpath)))
            element.clear()
            element.send_keys(vin_number)
        except TimeoutException:
            print(f"Name input field not found within {timeout} seconds")

    def click_on_the_next_button(self, timeout=10):
        try:
            wait = WebDriverWait(self.driver, timeout=10, poll_frequency=1, ignored_exceptions=[NoSuchElementException])
            element = wait.until(ec.visibility_of_element_located((By.XPATH, self.Next_button_xpath)))
            element.click()

        except TimeoutException:
            print(f"Name input field not found within {timeout} seconds")

            """
            This is for the reading and changing of the status of a beneficiary
            """

    def read_the_status_of_the_beneficiary(self, timeout=10):
        try:
            wait = WebDriverWait(self.driver, timeout=10, poll_frequency=1, ignored_exceptions=[NoSuchElementException])
            element = wait.until(ec.visibility_of_element_located((By.XPATH, self.Beneficiary_status_xpath )))
            status = element.text
            return status
        except TimeoutException:
            print(f"Name input field not found within {timeout} seconds")

    def change_the_status_of_beneficiary(self, timeout=10):
        try:
            wait = WebDriverWait(self.driver, timeout=10, poll_frequency=1, ignored_exceptions=[NoSuchElementException])
            element = wait.until(ec.visibility_of_element_located((By.XPATH, self.Deactivate_ana_activate_beneficiary_button_xpath)))
            element.click()
        except TimeoutException:
            print(f"Name input field not found within {timeout} seconds")
