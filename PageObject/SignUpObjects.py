from selenium import webdriver
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class SignupObjects:
    # Locators for various elements on the signup page
    name_id = "name"
    email_id = "email"
    password_id = "password"
    confirm_password_id = "comfirmPassword"
    sign_up_id = "btn-sign-up mt-1"
    login_link_xpath = "//a[normalize-space()='Login']"

    def __init__(self, driver):
        # Initialize the driver
        self.driver = driver

    def input_name(self, name_input, timeout=10):
        """
        Input name into the name field.
        Wait up to `timeout` seconds for the element to be visible.
        """
        try:
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=1, ignored_exceptions=[NoSuchElementException])
            element = wait.until(EC.visibility_of_element_located((By.ID, self.name_id)))
            element.clear()
            element.send_keys(name_input)
        except TimeoutException:
            print(f"Name input field not found within {timeout} seconds")

    def input_email(self, email_input, timeout=10):
        """
        Input email into the email field.
        Wait up to `timeout` seconds for the element to be visible.
        """
        try:
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=1, ignored_exceptions=[NoSuchElementException])
            element = wait.until(EC.visibility_of_element_located((By.ID, self.email_id)))
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
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=1, ignored_exceptions=[NoSuchElementException])
            element = wait.until(EC.visibility_of_element_located((By.ID, self.password_id)))
            element.clear()
            element.send_keys(password_input)
        except TimeoutException:
            print(f"Password input field not found within {timeout} seconds")

    def input_confirm_password(self, confirm_password_input, timeout=10):
        """
        Input confirm password into the confirm password field.
        Wait up to `timeout` seconds for the element to be visible.
        """
        try:
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=1, ignored_exceptions=[NoSuchElementException])
            element = wait.until(EC.visibility_of_element_located((By.ID, self.confirm_password_id)))
            element.clear()
            element.send_keys(confirm_password_input)
        except TimeoutException:
            print(f"Confirm password input field not found within {timeout} seconds")

    def click_on_the_signup_button(self, timeout=10):
        """
        Click the sign-up button.
        Wait up to `timeout` seconds for the element to be clickable.
        """
        try:
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=1, ignored_exceptions=[NoSuchElementException])
            element = wait.until(EC.element_to_be_clickable((By.ID, self.sign_up_id)))
            element.click()
        except TimeoutException:
            print(f"Sign-up button not found within {timeout} seconds")

    def click_on_the_login_link(self, timeout=10):
        """
        Click the login link.
        Wait up to `timeout` seconds for the element to be clickable.
        """
        try:
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=1, ignored_exceptions=[NoSuchElementException])
            element = wait.until(EC.element_to_be_clickable((By.XPATH, self.login_link_xpath)))
            element.click()
        except TimeoutException:
            print(f"Login link not found within {timeout} seconds")

    def email_generator(self):
        # Generate a random email address
        validchars = 'abcdefghijklmnopqrstuvwxyz1234567890'
        loginlen = random.randint(6, 15)
        login = ''
        for i in range(loginlen):
            pos = random.randint(0, len(validchars) - 1)
            login = login + validchars[pos]
        if login[0].isnumeric():
            pos = random.randint(0, len(validchars) - 10)
            login = validchars[pos] + login
        servers = ['@gmail', '@yahoo', '@redmail', '@hotmail', '@bing']
        servpos = random.randint(0, len(servers) - 1)
        email = login + servers[servpos]
        tlds = ['.com', '.in', '.gov', '.ac.in', '.net', '.org']
        tldpos = random.randint(0, len(tlds) - 1)
        email = email + tlds[tldpos]

        return email

    def generatePaassword(self):
        validchars = 'abcdefghijklmnopqrstuvwxyz1234567890'
        passwordlen = random.randint(6, 15)
        password = ''

        for i in range(passwordlen):
            pos = random.randint(0, len(validchars) - 1)
            password = password + validchars[pos]
            if password[0].isnumeric():
                pos = random.randint(0, len(validchars) - 10)
                password = validchars[pos] + password

        specialCharacter = ["?", "@", "#", "$", "%", "&"]
        choice = random.randint(0, len(specialCharacter) - 1)
        password = password + specialCharacter[choice]

        # Randomly select a non-numeric character for capitalization
        alpha_indices = [i for i, char in enumerate(password) if char.isalpha()]
        if alpha_indices:
            letter = random.choice(alpha_indices)
            password = password[:letter] + password[letter].upper() + password[letter + 1:]

        return password