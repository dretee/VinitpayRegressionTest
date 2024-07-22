# Import necessary modules and classes
import time
import requests
from Utilities import ReadXyfile
from selenium.webdriver.common.by import By
from Utilities.RecordLogger import RecordLogger
from Utilities.ReadProperties import ReadProperties
from PageObject.LoginObjects import LoginObjects

# to run the test use:   pytest -v -s TestCases/invalidLoginTestCase.py--browser chrome to run and also generate
# the html report use: pytest -v -s --html=Reports\reports.html TestCases/validLoginTestCase.py --browser chrome
"""
Negative test cases for the login page

Verify that a user cannot log in with an incorrect password.
Verify that a user cannot log in with an email that does not exist in the system.
Verify that a user cannot log in with an empty password field and email field.
Verify that a user cannot log in with an email containing special characters.
Verify the system's behavior after multiple failed login attempts.

"""


class Test_Login:
    # Initialize class variables with URLs, logger instance, and Excel file path
    URL = ReadProperties.getTestPageURL()  # Get main page URL from configuration
    ProductionURL = ReadProperties.getProductionPageURL()
    # loginPageUrl = ReadProperties.LoginURL()  # Get login page URL from configuration
    User_email, UserPassword = ReadProperties.getUserDetails()
    EXISTING_EMAIL = User_email  # Get existing email from configuration
    EXISTING_PASSWORD = UserPassword  # Get existing password
    # from configuration
    logger = RecordLogger.log_generator_info()  # Initialize logger instance
    PATH = ".\\TestData\\vnitpay data.xlsx"  # Excel file path

    # Method to log the start of a test
    def log_test_start(self, test_name):
        self.logger.info(f"****** STARTING TEST: {test_name} ******")

    # Method to log the end of a test
    def log_test_end(self, test_name):
        self.logger.info(f"****** ENDING TEST: {test_name} ******")

    # Method to open the website
    def open_website(self, setup, url):
        self.log_test_start("Open Website")
        self.driver = setup
        self.driver.get(url)
        self.driver.maximize_window()
        self.log_test_end("Open Website")

    # Test invalid login.
    # Verify that a user cannot log in with an incorrect password.
    def test_the_login_of_users_with_wrong_password(self, setup):
        try:
            self.log_test_start("***** Verify that a user cannot log in with an incorrect password *****")
            self.open_website(setup, self.URL)
            self.LO = LoginObjects(self.driver)
            self.LO.input_email(self.EXISTING_EMAIL)
            self.LO.input_password("1232123")
            self.LO.click_on_the_signin_button()
            time.sleep(3)

            error_message = "Invalid username or password"
            assert error_message in self.driver.find_element(By.TAG_NAME, "body").text, self.logger.info(
                "*** TEST FAILED: THE USER WAS LOGGED INTO THE ACCOUNT ****")

            self.logger.info("**** TEST PASSED: THE USER WAS NOT LOGGED INTO THE ACCOUNT  *****")

        except AssertionError:
            self.logger.error("Assertion Error: Test condition failed.")
            raise  # Re-raise the exception to indicate test failure

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise  # Re-raise the exception to indicate test failure

        finally:
            self.log_test_end("******* Verify that a user cannot log in with an incorrect password *******")
            self.driver.quit()

    # Verify that a user cannot log in with an email that does not exist in the system.
    def test_the_login_of_users_with_wrong_email(self, setup):
        try:
            self.log_test_start(
                "***** Verify that a user cannot log in with an email that does not exist in the system. *****")
            self.open_website(setup, self.URL)
            self.LO = LoginObjects(self.driver)
            self.LO.input_email("Uyahanthony@gmail.com")
            self.LO.input_password(self.EXISTING_PASSWORD)
            self.LO.click_on_the_signin_button()
            time.sleep(3)

            error_message = "Invalid username or password"
            assert error_message in self.driver.find_element(By.TAG_NAME, "body").text, self.logger.info(
                "*** TEST FAILED: THE USER WAS LOGGED INTO THE ACCOUNT ****")

            self.logger.info("**** TEST PASSED: THE USER WAS NOT LOGGED INTO THE ACCOUNT  *****")

        except AssertionError:
            self.logger.error("Assertion Error: Test condition failed.")
            raise  # Re-raise the exception to indicate test failure

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise  # Re-raise the exception to indicate test failure

        finally:
            self.log_test_end(
                "******* Verify that a user cannot log in with an email that does not exist in the system. *******")
            self.driver.quit()

    # Verify that a user cannot log in with an empty password field and missing email field.
    def test_the_login_of_users_with_missing_password_and_missing_email(self, setup):
        try:
            self.log_test_start("***** Verify that a user cannot log in with an empty password field and missing "
                                "email field.*****")
            self.open_website(setup, self.URL)
            self.LO = LoginObjects(self.driver)
            self.LO.input_email(self.EXISTING_EMAIL)
            self.LO.click_on_the_signin_button()
            time.sleep(3)

            error_message = "Password Is required"
            assert error_message in self.driver.find_element(By.TAG_NAME, "body").text, self.logger.info(
                "*** TEST FAILED: THE USER WAS LOGGED INTO THE ACCOUNT ****")

            self.driver.find_element(By.ID, self.LO.email_id).clear()
            self.LO.input_password(self.EXISTING_PASSWORD)
            self.LO.click_on_the_signin_button()
            time.sleep(2)
            error_message = "Username is required"
            assert error_message in self.driver.find_element(By.TAG_NAME, "body").text, self.logger.info(
                "*** TEST FAILED: THE USER WAS LOGGED INTO THE ACCOUNT ****")

            self.logger.info("**** TEST PASSED: THE USER WAS NOT LOGGED INTO THE ACCOUNT  *****")

        except AssertionError:
            self.logger.error("Assertion Error: Test condition failed.")
            raise  # Re-raise the exception to indicate test failure

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise  # Re-raise the exception to indicate test failure

        finally:
            self.log_test_end("******* Verify that a user cannot log in with an empty password field. *******")
            self.driver.quit()

    def test_the_login_of_users_with_email_with__special_charater(self, setup):
        try:
            self.log_test_start(
                "***** Verify that a user can log in with an email containing special characters.. *****")
            self.open_website(setup, self.URL)
            self.LO = LoginObjects(self.driver)
            self.LO.input_email("bassey+jay11@gmail.com")
            self.LO.input_password(self.EXISTING_PASSWORD)
            self.LO.click_on_the_signin_button()
            time.sleep(3)

            error_message = "Invalid username or password"
            assert error_message in self.driver.find_element(By.TAG_NAME, "body").text, self.logger.info(
                "*** TEST FAILED: THE USER WAS LOGGED INTO THE ACCOUNT ****")

            self.logger.info("**** TEST PASSED: THE USER WAS NOT LOGGED INTO THE ACCOUNT  *****")

        except AssertionError:
            self.logger.error("Assertion Error: Test condition failed.")
            raise  # Re-raise the exception to indicate test failure

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise  # Re-raise the exception to indicate test failure

        finally:
            self.log_test_end(
                "******* Verify that a user cannot log in with an email that does not exist in the system. *******")
            self.driver.quit()

    def test_the_login_of_users_tries_too_many_times(self, setup):
        try:
            self.log_test_start(
                "***** Verify that a user is blocked after too many login attempts *****")
            self.open_website(setup, self.URL)
            self.LO = LoginObjects(self.driver)

            # Attempt to log in 5 times
            for attempt in range(5):
                self.LO.input_email(self.EXISTING_EMAIL)
                self.LO.input_password("Password?")  # Use an incorrect password to trigger the failure
                self.LO.click_on_the_signin_button()
                time.sleep(3)  # Wait for the page to process the login attempt
                self.logger.info(f"Attempt {attempt + 1}: Tried logging in with incorrect password")

            # Check for the blocking message after the 5th attempt
            error_message = "Your account has been blocked due to too many failed login attempts."
            body_text = self.driver.find_element(By.TAG_NAME, "body").text
            if error_message in body_text:
                self.logger.info("**** TEST PASSED: THE USER WAS BLOCKED AFTER TOO MANY FAILED ATTEMPTS *****")
            else:
                self.logger.error("*** TEST FAILED: THE USER WAS NOT BLOCKED AFTER TOO MANY FAILED ATTEMPTS ***")
                assert error_message in body_text

        except AssertionError:
            self.logger.error("Assertion Error: Test condition failed.")
            raise  # Re-raise the exception to indicate test failure

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise  # Re-raise the exception to indicate test failure

        finally:
            self.log_test_end(
                "******* Verify that a user is blocked after too many login attempts *******")
            self.driver.quit()

    def test_All_Links_on_the_login_Page_(self, setup):
        # Start the test and log the information
        try:
            self.logger.info("************** TEST START **************")
            self.logger.info("*************** Login Page Links Functionality Verification *********** ")

            # Initialize the WebDriver
            self.open_website(setup, self.URL)
            self.LO = LoginObjects(self.driver)
            time.sleep(3)

            # Get all links on the page
            all_links = self.driver.find_elements(By.TAG_NAME, "a")
            self.logger.info(f"The total number of links on this page is {len(all_links)}")

            # Initialize counters for broken and functional links
            count_broken = 0
            count_functional = 0

            # Iterate through all links and check their status
            for link in all_links:
                url = link.get_attribute("href")
                try:
                    response = requests.head(url)
                except:
                    response = None

                if response is not None and response.status_code >= 400:
                    count_broken += 1
                    self.logger.info(f"THIS LINK {link} IS BROKEN")
                    print(f"THIS LINK {link} IS BROKEN")
                else:
                    count_functional += 1
                    self.logger.info(f"THIS LINK {link} IS FUNCTIONAL")
                    print(f"THIS LINK {link} IS FUNCTIONAL")

            # Log the total number of broken and functional links
            self.logger.info(f"TOTAL BROKEN LINKS: {count_broken}")
            self.logger.info(f"TOTAL FUNCTIONAL LINKS: {count_functional}")

            # Assert that there are no broken links
            assert count_broken == 0, "TEST FAILED: THERE ARE BROKEN LINKS ON THE PAGE"
            self.logger.info("TEST PASSED: ALL LINKS ARE FUNCTIONAL")

        except Exception as e:
            # Log any exceptions that occur during the test
            self.logger.error(f"Exception occurred: {str(e)}")
            assert False, f"Test failed due to exception: {str(e)}"
