import time

from selenium.webdriver.common.by import By
from Utilities.RecordLogger import RecordLogger
from Utilities.ReadProperties import ReadProperties

from PageObject.SignUpObjects import SignupObjects
from PageObject.LoginObjects import LoginObjects

"""
pytest -v -s TestCases/RegisterTestCases.py --browser chrome
pytest -v -s --html=Reports\reports1.html TestCases/RegisterTestCases.py --browser chrome
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

    def test_Registration_of_Account_with_valid_Details_001(self, setup):
        try:
            # Navigate to the signup page
            Page_object = self.Signup_Page_Navigator(setup)
            self.LO.click_on_the_register_link()

            # Fill in the form with valid details
            Page_object.input_name("John Doe")
            password = Page_object.generatePaassword()
            email = Page_object.email_generator()
            Page_object.input_email(email)
            Page_object.input_password(password)
            Page_object.input_confirm_password(password)

            # Submit the form
            Page_object.click_on_the_signup_button()
            time.sleep(10)

            # Check for the success messages
            message1, message2 = ("Hi 👋, Welcome to vnitpay",
                                  "Please check you email for a verification link to activate your account")

            assert message1 and message2 in self.driver.find_element(By.TAG_NAME, "body").text, self.logger.info(
                "**** TEST FAILED: USER'S ACCOUNT WAS NOT CREATED ***")
            self.logger.info("***** TEST PASSED: USER'S ACCOUNT WAS CREATED *****")

        except AssertionError:
            self.logger.error("Assertion Error: User's account was not created as expected.")
            raise  # Re-raise the exception to indicate test failure

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise  # Re-raise the exception to indicate test failure

        finally:
            self.driver.quit()

    def test_Registration_of_Account_with_already_registered_email_002(self, setup):
        try:
            Page_object = self.Signup_Page_Navigator(setup)
            self.LO.click_on_the_register_link()
            Page_object.input_name("John Doe")
            password = Page_object.generatePaassword()
            Page_object.input_email("basseyjay11@gmail.com")
            Page_object.input_password(password)
            Page_object.input_confirm_password(password)

            Page_object.click_on_the_signup_button()
            time.sleep(2)
            error_message = "User already exists"
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

    def test_Registration_of_Account_with_Different_Passwords_002(self, setup):
        try:
            Page_object = self.Signup_Page_Navigator(setup)
            self.LO.click_on_the_register_link()
            Page_object.input_name("John Doe")
            password1, password2 = Page_object.generatePaassword(), Page_object.generatePaassword()
            email = Page_object.email_generator()
            Page_object.input_email(email)
            Page_object.input_password(password1)
            Page_object.input_confirm_password(password2)

            Page_object.click_on_the_signup_button()
            time.sleep(2)
            error_message = "Password and confirm password must match"
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

    def test_Registration_of_Account_with_Password_Length_Lower_Than_6_Characters_003(self, setup):
        try:
            Page_object = self.Signup_Page_Navigator(setup)
            self.LO.click_on_the_register_link()
            Page_object.input_name("John Doe")
            password = "Vnit?"
            email = Page_object.email_generator()
            Page_object.input_email(email)
            Page_object.input_password(password)
            Page_object.input_confirm_password(password)

            Page_object.click_on_the_signup_button()
            time.sleep(3)
            error_message = "Password must be at least 8 characters"
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

    def est_Registration_of_Account_with_missing_confirm_password_001(self, setup):
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

