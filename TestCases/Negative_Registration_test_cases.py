import time

import pytest
from selenium.webdriver.common.by import By
from Utilities.RecordLogger import RecordLogger
from Utilities.ReadProperties import ReadProperties

from PageObject.SignUpObjects import SignupObjects
from PageObject.LoginObjects import LoginObjects

"""
pytest -v -s TestCases/Positive_Register_Test_Cases.py --browser chrome
pytest -v -s --html=Reports\reports1.html TestCases/Positive_Register_Test_Cases.py --browser chrome
"""


class Test_fo_Registration_of_new_user:
    URL = ReadProperties.getTestPageURL()  # Get main page URL from configuration
    ProductionURL = ReadProperties.getProductionPageURL()
    logger = RecordLogger.log_generator_info()

    Emails = []
    Names = []

    def log_test_start(self, test_name):
        self.logger.info(f"****** STARTING TEST: {test_name} ******")

    # Method to log the end of a test
    def log_test_end(self, test_name):
        self.logger.info(f"****** ENDING TEST: {test_name} ******")

    # Method to open the website
    def Signup_Page_Navigator(self, setup):
        self.driver = setup
        self.driver.get(self.URL)
        self.driver.maximize_window()
        self.signUp = SignupObjects(self.driver)
        self.LO = LoginObjects(self.driver)
        return self.signUp


    def test_Registration_of_Account_with_missing_name_001(self, setup):
        try:
            Page_object = self.Signup_Page_Navigator(setup)
            self.LO.click_on_the_register_link()
            password = Page_object.generatePaassword()
            email = Page_object.email_generator()
            Page_object.input_email(email)
            Page_object.input_password(password)
            Page_object.input_confirm_password(password)

            error_message = "lastname and firstname is missing"
            assert error_message in self.driver.find_element(By.TAG_NAME, "body").text, self.logger.info(
                "**** TEST FAILED: USER'S ACCOUNT WAS CREATED ***")

            # Test for just one name in the name field
            Page_object.input_name("John")
            error_message = "lastname and firstname is missing"
            assert error_message in self.driver.find_element(By.TAG_NAME, "body").text, self.logger.info(
                "**** TEST FAILED: USER'S ACCOUNT WAS CREATED ***")

            self.logger.info("***** TEST PASSED: USER'S ACCOUNT WAS NOT CREATED *****")

        except AssertionError:
            self.logger.error("Assertion Error: User's account was created when it should not have been.")
            raise  # Re-raise the exception to indicate test failure

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise  # Re-raise the exception to indicate test failure

        finally:
            self.driver.quit()

    def test_Registration_of_Account_with_missing_email_001(self, setup):
        try:
            Page_object = self.Signup_Page_Navigator(setup)
            self.LO.click_on_the_register_link()
            Page_object.input_name("John Doe")
            password = Page_object.generatePaassword()
            Page_object.input_password(password)
            Page_object.input_confirm_password(password)

            error_message = "Email is missing"
            assert error_message in self.driver.find_element(By.TAG_NAME, "body").text, self.logger.info(
                "**** TEST FAILED: USER'S ACCOUNT WAS CREATED ***")
            self.logger.info("***** TEST PASSED: USER'S ACCOUNT WAS NOT CREATED *****")

        except AssertionError:
            self.logger.error("Assertion Error: User's account was created when it should not have been.")
            raise  # Re-raise the exception to indicate test failure

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise  # Re-raise the exception to indicate test failure

        finally:
            self.driver.quit()

    def test_Registration_of_Account_with_missing_password_001(self, setup):
        try:
            Page_object = self.Signup_Page_Navigator(setup)
            self.LO.click_on_the_register_link()
            Page_object.input_name("John Doe")
            password = Page_object.generatePaassword()
            email = Page_object.email_generator()
            Page_object.input_email(email)
            Page_object.input_confirm_password(password)

            error_message = "password is missing"
            assert error_message in self.driver.find_element(By.TAG_NAME, "body").text, self.logger.info(
                "**** TEST FAILED: USER'S ACCOUNT WAS CREATED ***")
            self.logger.info("***** TEST PASSED: USER'S ACCOUNT WAS NOT CREATED *****")

        except AssertionError:
            self.logger.error("Assertion Error: User's account was created when it should not have been.")
            raise  # Re-raise the exception to indicate test failure

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise  # Re-raise the exception to indicate test failure

        finally:
            self.driver.quit()

    def test_Registration_of_Account_with_missing_confirm_password_001(self, setup):
        try:
            # Navigate to the signup page
            Page_object = self.Signup_Page_Navigator(setup)
            self.LO.click_on_the_register_link()

            # Fill in the form
            Page_object.input_name("John Doe")
            password = Page_object.generatePaassword()
            email = Page_object.email_generator()
            Page_object.input_email(email)
            Page_object.input_password(password)

            # Check for the error message
            error_message = "password is missing"
            page_text = self.driver.find_element(By.TAG_NAME, "body").text

            assert error_message in page_text, self.logger.info(
                "**** TEST FAILED: USER'S ACCOUNT WAS CREATED ***")
            self.logger.info("***** TEST PASSED: USER'S ACCOUNT WAS NOT CREATED *****")

        except AssertionError:
            self.logger.error("Assertion Error: User's account was created when it should not have been.")
            raise  # Re-raise the exception to indicate test failure

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise  # Re-raise the exception to indicate test failure

        finally:
            self.driver.quit()

    test_data = [
            ("anthony123?", "Password must contain at least one uppercase letter."),
            ("Anthiny123", "Password must contain at least one non-alphanumeric character."),
            ("Anthony?", "Password must contain at least one digit."),
            ("1232345A?", "Password must contain at least one lowercase letter."),
            ("qVRT1?", "Password must be at least 8 characters long.")
]
    @pytest.mark.parametrize("Password, error_message", test_data)
    def test_verify_that_the_password_contains_all_necessary_character(self, setup, Password, error_message):
        try:
            Page_object = self.Signup_Page_Navigator(setup)
            self.LO.click_on_the_register_link()
            Page_object.input_name("John Doe")
            Page_object.input_email(Page_object.email_generator())
            Page_object.input_password(Password)
            Page_object.input_confirm_password(Password)

            body_text = self.driver.find_element(By.TAG_NAME, "body").text
            assert error_message in body_text, self.logger.info("***** TEST FAILED ******")
            self.logger.info("***** TEST PASSED ******")

        except AssertionError:
            self.logger.error("Assertion Error: User's account was created when it should not have been.")
            raise  # Re-raise the exception to indicate test failure

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise  # Re-raise the exception to indicate test failure

        finally:
            self.driver.quit()







