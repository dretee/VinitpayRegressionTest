import time

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

    # Method to open the website
    def Signup_Page_Navigator(self, setup):
        self.driver = setup
        self.driver.get(self.URL)
        self.driver.maximize_window()
        self.signUp = SignupObjects(self.driver)
        self.LO = LoginObjects(self.driver)
        return self.signUp

    def test_Registration_of_Account_with_valid_Details_001(self, setup, log_test_end, log_test_start):
        try:
            # Logging the beginning of the test case
            log_test_start ("**** Verify the creation of accounts with valid data ****")
            # Navigate to the signup page
            Signup_controller = self.Signup_Page_Navigator(setup)
            self.LO.click_on_the_register_link()

            #checking if the login link is functional on the sign up page
            Signup_controller.click_on_the_login_link()
            message = "Log in to your Vnitpay account"

            body_text = self.driver.find_element(By.TAG_NAME, "body").text
            assert message in body_text, self.logger.info(
                "**** TEST FAILED: PAGE WAS NOT FOUND ***")
            self.logger.info("***** TEST PASSED: SIGN IN PAGE WAS FOUND *****")

            time.sleep(3)
            self.LO.click_on_the_register_link()

            # Fill in the form with valid details
            Signup_controller.input_name("John Doe")
            password = Signup_controller.generatePaassword()
            Signup_controller.input_email(Signup_controller.email_generator())
            Signup_controller.input_password(password)
            Signup_controller.input_confirm_password(password)

            # Submit the form
            Signup_controller.click_on_the_signup_button()
            time.sleep(10)

            # Check for the success messages
            message1, message2 = ("Hi 👋, Welcome to vnitpay",
                                  "Please check you email for a verification link to activate your account")

            assert message1 and message2 in body_text, self.logger.info(
                "**** TEST FAILED: USER'S ACCOUNT WAS NOT CREATED ***")
            self.logger.info("***** TEST PASSED: USER'S ACCOUNT WAS CREATED *****")

        except AssertionError:
            self.logger.error("Assertion Error: User's account was not created as expected.")
            raise  # Re-raise the exception to indicate test failure

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise  # Re-raise the exception to indicate test failure

        finally:
            log_test_end("***TEST HAS ENDED***")
            self.driver.quit()

    def test_Registration_of_Account_with_already_registered_email_002(self, setup, log_test_start, log_test_end):
        try:
            log_test_start("**** Verify the creation of a user with the data of an existing user ****")
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
            log_test_end("***TEST IS ENDED***")
            self.driver.quit()

    def test_Registration_of_Account_with_Different_Passwords_002(self, setup,log_test_start, log_test_end):
        try:
            log_test_start("**** Verify the creation of a user with different passwords****")
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
            log_test_end("***TEST IS ENDED***")
            self.driver.quit()


