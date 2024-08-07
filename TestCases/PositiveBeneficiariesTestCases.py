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
Test cases for the beneficiary page

Verify the response of the system when the user click on the proceed button without filling any of the field on the other beneficiary creation 
Verify the response of the system when any of the fields are left empty 
Verify the deactivation of a other beneficiary 
Verify the activation of a other beneficiary
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

    def est_the_functionality_of_the_beneficiary_navigation(self, setup):
        try:
            # Initialize Beneficiary page objects
            self.log_test_start("Test_the_functionality_of_the_beneficiary_navigation")
            self.open_website_and_log_in_user(setup, self.URL)

            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)
            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()
            time.sleep(5)
            Common_text_on_page = "New Beneficiary"
            assert Common_text_on_page in self.driver.find_element(By.TAG_NAME, "body").text, self.logger.info(
                "**** TEST FAILED: USER'S ACCOUNT WAS NOT CREATED ***")
            self.logger.info("***** TEST PASSED: USER'S ACCOUNT WAS CREATED *****")

        except AssertionError:
            self.logger.error("Assertion Error: this is not the page the user intends to go to.")
            raise
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise
        finally:
            self.driver.quit()

    def est_creation_of_new_other_beneficiary_filling_phone_number_fields(self, setup):
        """Test the creation of a new beneficiary without filling the required fields."""
        try:
            self.log_test_start("Testing creation of new beneficiary with missing fields.")
            self.open_website_and_log_in_user(setup, self.URL)

            # Initialize Beneficiary page objects
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)

            # Navigate to beneficiary creation page

            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()
            time.sleep(3)
            self.Beneficiary_page_objects.click_on_the_new_beneficiary_button()
            time.sleep(3)
            self.Beneficiary_page_objects.click_on_the_other_beneficiary_option()

            self.Beneficiary_page_objects.input_phone_number("08065748322")

            self.Beneficiary_page_objects.click_on_the_proceed_button()

            # Test various scenarios of field completion
            expected_message = "All fields are required"
            assert expected_message in self.driver.find_element(By.TAG_NAME, "body").text, self.logger.info(
                "**** TEST FAILED: USER'S ACCOUNT WAS NOT CREATED ***")
            self.logger.info("***** TEST PASSED: REQUIRED FIELDS VALIDATION WORKS *****")

        except AssertionError:
            self.logger.error("Assertion Error: User's account was not created as expected.")
            raise

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

        finally:
            self.driver.quit()

    def est_creation_of_new_other_beneficiary_filling_First_Name_fields(self, setup):
        """Test the creation of a new beneficiary without filling the required fields."""
        try:
            self.log_test_start("Testing creation of new beneficiary with missing fields.")
            self.open_website_and_log_in_user(setup, self.URL)

            # Initialize Beneficiary page objects
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)

            # Navigate to beneficiary creation page
            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()
            time.sleep(3)
            self.Beneficiary_page_objects.click_on_the_new_beneficiary_button()
            time.sleep(3)
            self.Beneficiary_page_objects.click_on_the_other_beneficiary_option()

            First_name, _ = SignupObjects(self.driver).generate_names()
            self.Beneficiary_page_objects.input_first_name(First_name)

            self.Beneficiary_page_objects.click_on_the_proceed_button()

            # Test various scenarios of field completion
            expected_message = "All fields are required"
            assert expected_message in self.driver.find_element(By.TAG_NAME, "body").text, self.logger.info(
                "**** TEST FAILED: USER'S ACCOUNT WAS NOT CREATED ***")
            self.logger.info("***** TEST PASSED: REQUIRED FIELDS VALIDATION WORKS *****")

        except AssertionError:
            self.logger.error("Assertion Error: User's account was not created as expected.")
            raise

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

        finally:
            self.driver.quit()

    def est_creation_of_new_other_beneficiary_filling_Last_Name_fields(self, setup):
        """Test the creation of a new beneficiary without filling the required fields."""
        try:
            self.log_test_start("Testing creation of new beneficiary with missing fields.")
            self.open_website_and_log_in_user(setup, self.URL)

            # Initialize Beneficiary page objects
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)

            # Navigate to beneficiary creation page
            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()
            time.sleep(3)
            self.Beneficiary_page_objects.click_on_the_new_beneficiary_button()
            time.sleep(3)
            self.Beneficiary_page_objects.click_on_the_other_beneficiary_option()
            _, Last_name = SignupObjects(self.driver).generate_names()
            self.Beneficiary_page_objects.input_first_name(Last_name)

            self.Beneficiary_page_objects.click_on_the_proceed_button()

            # Test various scenarios of field completion
            expected_message = "All fields are required"
            assert expected_message in self.driver.find_element(By.TAG_NAME, "body").text, self.logger.info(
                "**** TEST FAILED: USER'S ACCOUNT WAS NOT CREATED ***")
            self.logger.info("***** TEST PASSED: REQUIRED FIELDS VALIDATION WORKS *****")

        except AssertionError:
            self.logger.error("Assertion Error: User's account was not created as expected.")
            raise

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

        finally:
            self.driver.quit()

    def est_creation_of_new_other_beneficiary_filling_email_fields(self, setup):
        """Test the creation of a new beneficiary without filling the required fields."""
        try:
            self.log_test_start("Testing creation of new beneficiary with missing fields.")
            self.open_website_and_log_in_user(setup, self.URL)

            # Initialize Beneficiary page objects
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)

            # Navigate to beneficiary creation page
            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()
            time.sleep(3)
            self.Beneficiary_page_objects.click_on_the_new_beneficiary_button()
            self.Beneficiary_page_objects.click_on_the_other_beneficiary_option()

            self.Beneficiary_page_objects.input_email(SignupObjects(self.driver).email_generator())
            time.sleep(3)
            self.Beneficiary_page_objects.click_on_the_proceed_button()

            # Test various scenarios of field completion
            expected_message = "All fields are required"
            assert expected_message in self.driver.find_element(By.TAG_NAME, "body").text, self.logger.info(
                "**** TEST FAILED: USER'S ACCOUNT WAS NOT CREATED ***")
            self.logger.info("***** TEST PASSED: REQUIRED FIELDS VALIDATION WORKS *****")

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
            time.sleep(3)
            self.Beneficiary_page_objects.click_on_the_new_beneficiary_button()
            self.Beneficiary_page_objects.click_on_the_other_beneficiary_option()

            self.Beneficiary_page_objects.input_phone_number("08065748322")
            time.sleep(3)

            # Generate the names for the creation for the names of the new users
            First_name, Last_name = SignupObjects(self.driver).generate_names()
            self.Beneficiary_page_objects.input_first_name(First_name)
            time.sleep(3)
            self.Beneficiary_page_objects.input_last_name(Last_name)
            time.sleep(3)
            self.Beneficiary_page_objects.input_email(SignupObjects(self.driver).email_generator())

            self.Beneficiary_page_objects.click_on_the_proceed_button()

            creation_successful_message, name_of_beneficiary_on_table = (
                self.Beneficiary_page_objects.get_the_text_for_the_alert_to_the_user(),
                f"08065748322-{First_name} {Last_name}")

            """ Assertion for the successful on the table when the user is created
            assert creation_successful_message is "New Beneficiary record created successfully", self.logger.info(
                "**** TEST FAILED: USER'S ACCOUNT WAS NOT CREATED ***")
            self.logger.info("***** TEST PASSED: USER'S ACCOUNT WAS CREATED *****")
            """
            """ Assertion for the name logged on the table when the user is created"""
            assert self.driver.find_element(By.XPATH, "//tbody/tr[1]/td[3]").text == name_of_beneficiary_on_table, self.logger.info(
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

    def est_the_deactivation_of_beneficiary(self, setup):
        """
        Test the deactivation and reactivation process of a beneficiary within the application.
        This includes verifying the status changes and appropriate alert messages upon state changes.
        """
        try:
            # Initialization: Setup test logging and open the website
            self.log_test_start("Test_the_creation_of_new_other_beneficiary")
            self.open_website_and_log_in_user(setup, self.URL)

            # Beneficiary Page Setup: Access beneficiary management and prepare for interaction
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)
            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()

            # Deactivation Process: Change beneficiary status to 'Inactive'
            self.Beneficiary_page_objects.change_the_status_of_beneficiary()

            # Reactivation Process: Change beneficiary status back to 'Active'
            Deactivation_message, name_of_beneficiary = self.Beneficiary_page_objects.get_the_text_for_the_alert_to_the_user()
            time.sleep(5)
            """assert Deactivation_message == f"{name_of_beneficiary} deactivated", (
                self.logger.info("**** TEST FAILED: USER'S ACCOUNT WAS NOT CREATED ***")
            )
            self.logger.info("***** TEST PASSED: USER'S ACCOUNT WAS CREATED *****")
            time.sleep(3)
            """
            # Final Status Validation: Ensure the beneficiary is marked as 'Active'
            assert self.Beneficiary_page_objects.read_the_status_of_the_beneficiary() == "Inactive", (
                self.logger.info("**** TEST FAILED: USER'S ACCOUNT WAS NOT CREATED ***")
            )
            self.logger.info("***** TEST PASSED: USER'S ACCOUNT WAS CREATED *****")

            time.sleep(4)

            # Verification: Check deactivation alert message and beneficiary status
            Activation_message, name_of_beneficiary = self.Beneficiary_page_objects.get_the_text_for_the_alert_to_the_user()
            assert Activation_message == f"{name_of_beneficiary} activated successfully", (
                self.logger.info("**** TEST FAILED: USER'S ACCOUNT WAS NOT CREATED ***")
            )
            self.logger.info("***** TEST PASSED: USER'S ACCOUNT WAS CREATED *****")

            # Validate Status: Ensure the beneficiary is marked as 'Inactive'
            assert self.Beneficiary_page_objects.read_the_status_of_the_beneficiary() == "Active", (
                self.logger.info("**** TEST FAILED: USER'S ACCOUNT WAS NOT CREATED ***")
            )
            self.logger.info("***** TEST PASSED: USER'S ACCOUNT WAS CREATED *****")

        except AssertionError:
            # Error Handling: Log assertion errors and raise them for further investigation
            self.logger.error("Assertion Error: User's account was not created as expected.")
            raise

        except Exception as e:
            # Unexpected Error Handling: Log any unforeseen exceptions and raise them
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

        finally:
            # Cleanup: Ensure the browser session is properly closed, even if errors occur
            self.driver.quit()

    def test_the_activation_of_beneficiary(self, setup):
        """
        Test the deactivation and reactivation process of a beneficiary within the application.
        This includes verifying the status changes and appropriate alert messages upon state changes.
        """
        try:
            # Initialization: Setup test logging and open the website
            self.log_test_start("Test_the_creation_of_new_other_beneficiary")
            self.open_website_and_log_in_user(setup, self.URL)

            # Beneficiary Page Setup: Access beneficiary management and prepare for interaction
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)
            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()

            # Deactivation Process: Change beneficiary status to 'Inactive'
            self.Beneficiary_page_objects.change_the_status_of_beneficiary()
            time.sleep(4)

            # Verification: Check deactivation alert message and beneficiary status
            """Activation_message, name_of_beneficiary = self.Beneficiary_page_objects.get_the_text_for_the_alert_to_the_user()
            assert Activation_message == f"{name_of_beneficiary} activated sucessfully", (
                self.logger.info("**** TEST FAILED: USER'S ACCOUNT WAS NOT CREATED ***")
            )
            self.logger.info("***** TEST PASSED: USER'S ACCOUNT WAS CREATED *****")
"""
            # Validate Status: Ensure the beneficiary is marked as 'Inactive'
            assert self.Beneficiary_page_objects.read_the_status_of_the_beneficiary() == "Active", (
                self.logger.info("**** TEST FAILED: USER'S ACCOUNT WAS NOT CREATED ***")
            )
            self.logger.info("***** TEST PASSED: USER'S ACCOUNT WAS CREATED *****")

        except AssertionError:
            # Error Handling: Log assertion errors and raise them for further investigation
            self.logger.error("Assertion Error: User's account was not created as expected.")
            raise

        except Exception as e:
            # Unexpected Error Handling: Log any unforeseen exceptions and raise them
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

        finally:
            # Cleanup: Ensure the browser session is properly closed, even if errors occur
            self.driver.quit()
