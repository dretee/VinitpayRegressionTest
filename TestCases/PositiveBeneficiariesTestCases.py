# Import necessary modules and classes
import time
import requests
from Utilities import ReadXyfile
from selenium.webdriver.common.by import By
from Utilities.RecordLogger import RecordLogger
from Utilities.ReadProperties import ReadProperties
from PageObject.LoginObjects import LoginObjects
from PageObject.SignUpObjects import SignupObjects
from PageObject.BeneficiaryObject import BeneficiaryObjects

# to run the test use:   pytest -v -s TestCases/invalidLoginTestCase.py--browser chrome to run and also generate
# the html report use: pytest -v -s --html=Reports\reports.html TestCases/validLoginTestCase.py --browser chrome
"""
Negative test cases for the login page

Verify the response of the system when the user click on the proceed button without filling any of the field on the other beneficiary creation 
Verify the response of the system when any of the fields are left empty 
Verify the response of the system when a url, name and special characters are inputted in the phone number filed and other vaild data
Verify the response of the system when a url, email,  numbers and special characters (name with special characters) are inputted in the firstname and lastname filed and other vaild data
Verify the response of the system when a url, numbers and special characters (name with special characters) are inputted in the email filed and other vaild data

Verify the response of the system to a wrong reg number 
Verify the response to an empty field of the reg number 
Verify the response to an empty field of the vin number 
Verify the response of the system to a wrong vin number 


"""


class Test_Login:
    # Initialize class variables with URLs, logger instance, and Excel file path
    URL = ReadProperties.getTestPageURL()  # Get main page URL from configuration
    # loginPageUrl = ReadProperties.LoginURL()  # Get login page URL from configuration
    User_email, UserPassword = ReadProperties.getUserDetails()
    EXISTING_EMAIL = User_email  # Get existing email from configuration
    EXISTING_PASSWORD = UserPassword  # Get existing password
    # from configuration
    logger = RecordLogger.log_generator_info()  # Initialize logger instance

    # Method to log the start of a test
    def log_test_start(self, test_name):
        self.logger.info(f"****** STARTING TEST: {test_name} ******")

    # Method to log the end of a test
    def log_test_end(self, test_name):
        self.logger.info(f"****** ENDING TEST: {test_name} ******")

    # Method to open the website
    def open_website_and_log_in_user(self, setup, url):
        self.log_test_start("Open Website")
        self.driver = setup
        self.driver.get(url)
        self.driver.maximize_window()
        self.Login_page_objects = LoginObjects(self.driver)

        # Log in user into their account
        self.Login_page_objects.input_email(self.EXISTING_EMAIL)
        self.Login_page_objects.input_password(self.EXISTING_PASSWORD)
        self.Login_page_objects.click_on_the_signin_button()

        self.log_test_end("Open Website")

    def verify_field_requirements(self, beneficiary_page, phone=None, first_name=None, last_name=None):
        """Helper function to fill fields and verify required field validation."""
        if phone:
            beneficiary_page.input_phone_number(phone)
        if first_name:
            beneficiary_page.input_first_name(first_name)
        if last_name:
            beneficiary_page.input_last_name(last_name)

        beneficiary_page.click_on_the_proceed_button()

        # Check if the required fields message is displayed
        expected_message = "All fields are required"
        assert expected_message in self.driver.find_element(By.TAG_NAME, "body").text, self.logger.info(
            "**** TEST FAILED: USER'S ACCOUNT WAS NOT CREATED ***")
        self.logger.info("***** TEST PASSED: REQUIRED FIELDS VALIDATION WORKS *****")

    def test_the_functionality_of_the_beneficiary_navigation(self, setup):
        try:
            # Initialize Beneficiary page objects
            self.log_test_start("Test_the_functionality_of_the_beneficiary_navigation")
            self.open_website_and_log_in_user(setup, self.URL)

            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)
            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()

            Common_text_on_page = "New Beneficiary"
            assert Common_text_on_page in self.driver.find_element(By.TAG_NAME, "body").text, self.logger.info(
                "**** TEST FAILED: USER'S ACCOUNT WAS NOT CREATED ***")
            self.logger.info("***** TEST PASSED: USER'S ACCOUNT WAS CREATED *****")

        except AssertionError:
            self.logger.error("Assertion Error: this is not the page the user intends to go to.")
            raise
        except Exception as e:
            self.logger.error()
            raise
        finally:
            self.driver.quit(f"An unexpected error occurred: {e}")

    def test_creation_of_new_other_beneficiary_without_filling_fields(self, setup):
        """Test the creation of a new beneficiary without filling the required fields."""
        try:
            self.log_test_start("Testing creation of new beneficiary with missing fields.")
            self.open_website_and_log_in_user(setup, self.URL)

            # Initialize Beneficiary page objects
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)

            # Navigate to beneficiary creation page

            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()
            self.Beneficiary_page_objects.click_on_the_new_beneficiary_button()
            self.Beneficiary_page_objects.click_on_the_other_beneficiary_option()

            # Test various scenarios of field completion
            self.verify_field_requirements(self.Beneficiary_page_objects)
            self.verify_field_requirements(self.Beneficiary_page_objects, phone="08065748322")

            first_name, last_name = SignupObjects(self.driver).generate_names()
            self.verify_field_requirements(self.Beneficiary_page_objects, phone="08065748322", first_name=first_name)
            self.verify_field_requirements(self.Beneficiary_page_objects, phone="08065748322", first_name=first_name,
                                           last_name=last_name)

        except AssertionError:
            self.logger.error("Assertion Error: User's account was not created as expected.")
            raise

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

        finally:
            self.driver.quit()

    def test_the_creation_of_new_other_beneficiary(self, setup):
        try:
            self.log_test_start("Test_the_creation_of_new_other_beneficiary")
            self.open_website_and_log_in_user(setup, self.URL)
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)
            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()
            self.Beneficiary_page_objects.click_on_the_new_beneficiary_button()
            self.Beneficiary_page_objects.click_on_the_other_beneficiary_option()
            self.Beneficiary_page_objects.input_phone_number("08065748322")

            # Generate the names for the creation for the names of the new users
            First_name, Last_name = SignupObjects(self.driver).generate_names()
            self.Beneficiary_page_objects.input_first_name(First_name)
            self.Beneficiary_page_objects.input_last_name(Last_name)
            self.Beneficiary_page_objects.input_email(SignupObjects(self.driver).email_generator())

            self.Beneficiary_page_objects.click_on_the_proceed_button()

            creation_successful_message = f"08065748322-{First_name} {Last_name}"
            assert creation_successful_message in self.driver.find_element(By.TAG_NAME, "body").text, self.logger.info(
                "**** TEST FAILED: USER'S ACCOUNT WAS NOT CREATED ***")
            self.logger.info("***** TEST PASSED: USER'S ACCOUNT WAS CREATED *****")
        except AssertionError:
            self.logger.error("Assertion Error: User's account was not created as expected.")
            raise

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

        finally:
            self.driver.quit()
