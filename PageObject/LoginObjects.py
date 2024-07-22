from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class LoginObjects:
    # Locators for various elements on the login page
    welcomePage_Signin_xpath = "//a[normalize-space()='sign in']"
    logo_xpath = "//a[@id='logo']//*[name()='svg']"
    email_id = "email"
    password_id = "password"
    forgot_password_id = "forgotpassword"
    signin_button_selector = "button[type='submit']"
    register_link_xpath = "//a[normalize-space()='Register']"
    Logout_dropdown_id = "selected-merchant"
    Logout_button_Xpath = "//span[normalize-space()='logout']"
    error_message_xpath = "//div[@class='error-div']"

    def __init__(self, driver):
        # Initialize the driver
        self.driver = driver

    def locate_and_click_signin_button(self, timeout=10):
        """
        Locate and click the sign-in button on the welcome page.
        Wait up to `timeout` seconds for the element to be clickable.
        """
        try:
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=1,
                                 ignored_exceptions=[NoSuchElementException])
            element = wait.until(ec.element_to_be_clickable((By.XPATH, self.welcomePage_Signin_xpath)))
            element.click()
        except TimeoutException:
            print(f"Sign-in button not found within {timeout} seconds")

    def get_logo_location(self, timeout=10):
        """
        Get the location of the logo element.
        Wait up to `timeout` seconds for the element to be present.
        """
        try:
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=1,
                                 ignored_exceptions=[NoSuchElementException])
            element = wait.until(ec.presence_of_element_located((By.XPATH, self.logo_xpath)))
            return element.location
        except TimeoutException:
            print(f"Element with XPath {self.logo_xpath} not found within {timeout} seconds")
            return None

    def input_email(self, email_input, timeout=10):
        """
        Input email into the email field.
        Wait up to `timeout` seconds for the element to be visible.
        """
        try:
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=1,
                                 ignored_exceptions=[NoSuchElementException])
            element = wait.until(ec.visibility_of_element_located((By.ID, self.email_id)))
            element.clear()
            element.send_keys(email_input)
        except TimeoutException:
            print(f"Email input field not found within {timeout} seconds")

    def input_password(self, password_input, timeout=10):
        """
        Input password into the password field.
        Wait up to `timeout` seconds for the element to be visible.
        """
        try:
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=1,
                                 ignored_exceptions=[NoSuchElementException])
            element = wait.until(ec.visibility_of_element_located((By.ID, self.password_id)))
            element.clear()
            element.send_keys(password_input)
        except TimeoutException:
            print(f"Password input field not found within {timeout} seconds")

    def click_on_the_signin_button(self, timeout=5):
        """
        Click the sign-in button.
        Wait up to `timeout` seconds for the element to be clickable.
        """
        try:
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=1,
                                 ignored_exceptions=[NoSuchElementException])
            element = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, self.signin_button_selector)))
            element.click()
        except TimeoutException:
            print(f"Sign-in button not found within {timeout} seconds")

    def click_on_the_forgot_password(self, timeout=10):
        """
        Click the forgot password link.
        Wait up to `timeout` seconds for the element to be clickable.
        """
        try:
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=1,
                                 ignored_exceptions=[NoSuchElementException])
            element = wait.until(ec.element_to_be_clickable((By.ID, self.forgot_password_id)))
            element.click()
        except TimeoutException:
            print(f"Forgot password link not found within {timeout} seconds")

    def click_on_the_register_link(self, timeout=10):
        """
        Click the register link.
        Wait up to `timeout` seconds for the element to be clickable.
        """
        try:
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=1,
                                 ignored_exceptions=[NoSuchElementException])
            element = wait.until(ec.element_to_be_clickable((By.XPATH, self.register_link_xpath)))
            element.click()
        except TimeoutException:
            print(f"Register link not found within {timeout} seconds")

    def click_on_the_logout_button(self, timeout=10):
        """
        Method to click on the logging out of the application.
        """
        try:
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=1,
                                 ignored_exceptions=[NoSuchElementException])
            element = wait.until(ec.presence_of_element_located((By.ID, self.Logout_dropdown_id)))
            element.click()
            element = wait.until(ec.element_to_be_clickable((By.XPATH, self.Logout_button_Xpath)))
            element.click()
            time.sleep(10)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def error_alert(self):
        """
        Error message for wrong login with invalid details
        """
        wait = WebDriverWait(self.driver, timeout=10, poll_frequency=1, ignored_exceptions=[NoSuchElementException])
        element = wait.until(ec.presence_of_element_located((By.XPATH, self.error_message_xpath)))
        error_message = element.get_attribute("text")
        return error_message
