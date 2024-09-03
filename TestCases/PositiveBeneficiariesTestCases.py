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

    def test_the_functionality_of_the_beneficiary_navigation(self, setup):
        try:
            # Initialize Beneficiary page objects
            self.log_test_start("***** TEST THE FUNCTIONALITY OF THE BENEFICIARY NAVIGATION *****")
            self.open_website_and_log_in_user(setup, self.URL)

            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)
            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()
            time.sleep(5)
            self.logger.info("*****THE BENEFICIARY'S DATA LOGGING TABLE I SEEN WITH ALL THE BENEFICIARY *****")
            Common_text_on_page = "New Beneficiary"
            assert Common_text_on_page in self.driver.find_element(By.TAG_NAME, "body").text, self.logger.info(
                "**** TEST FAILED: USER'S ACCOUNT WAS NOT CREATED ***")
            self.logger.info("***** TEST PASSED: NAVIGATION TO THE BENEFICIARY PAGE IS FUNCTIONAL *****")

        except AssertionError:
            self.logger.error("Assertion Error: this is not the page the user intends to go to.")
            raise
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise
        finally:
            self.driver.quit()

    def test_the_Header_on_the_other_beneficiary_form(self, setup):
        try:
            # Initialize Beneficiary page objects
            self.log_test_start("Test_the_functionality_of_the_beneficiary_navigation")
            self.open_website_and_log_in_user(setup, self.URL)

            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)
            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()
            self.Beneficiary_page_objects.click_on_the_new_beneficiary_button()
            self.Beneficiary_page_objects.click_on_the_other_beneficiary_option()
            time.sleep(5)

            # CHECKING THE HEADER OF THE FORM FOR THE CREATION OF AN OTHER BENEFICIARY
            assert self.driver.find_element(By.XPATH, "//div[@id='__layout']//div//main//h2").text == "Beneficiary Details", self.logger.info(
                "**** TEST FAILED: USER'S ACCOUNT WAS NOT CREATED ***")
            self.logger.info("***** TEST PASSED: THE HEADER IS CORRECT*****")

        except AssertionError:
            self.logger.error("Assertion Error: this is not the page the user intends to go to.")
            raise
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise
        finally:
            self.driver.quit()

    def test_the_creation_of_new_other_beneficiary(self, setup):
        try:
            self.log_test_start("***** TESTING THE CREATION OF NEW OTHER BENEFICIARY.******")
            self.open_website_and_log_in_user(setup, self.URL)
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)

            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()
            time.sleep(3)
            self.Beneficiary_page_objects.click_on_the_new_beneficiary_button()
            self.Beneficiary_page_objects.click_on_the_other_beneficiary_option()
            phone_number = SignupObjects(self.driver).generate_phone_number()
            self.Beneficiary_page_objects.input_phone_number(phone_number)
            time.sleep(3)
            self.logger.info("***** USER INPUTS THE THE PHONE NUMBER IN THE CORRECT FIELD.******")
            # Generate the names for the creation for the names of the new users
            First_name, Last_name = SignupObjects(self.driver).generate_names()
            self.Beneficiary_page_objects.input_first_name(First_name)
            self.log_test_start("***** USER INPUTS THE THE FIRST NAME IN THE CORRECT FIELD.******")
            time.sleep(3)
            self.Beneficiary_page_objects.input_last_name(Last_name)
            self.log_test_start("***** USER INPUTS THE THE LAST NAME IN THE CORRECT FIELD.******")

            self.Beneficiary_page_objects.input_email(SignupObjects(self.driver).email_generator())
            self.log_test_start("***** USER INPUTS THE THE EMAIL IN THE CORRECT FIELD.******")
            self.Beneficiary_page_objects.click_on_the_proceed_button()
            self.log_test_start("***** USER CLICKS ON THE PROCEED BUTTON.******")

            name_of_beneficiary_on_table = f"{phone_number} - {First_name} {Last_name}"
            time.sleep(5)
            """ Assertion for the name logged on the table when the user is created"""
            assert self.driver.find_element(By.XPATH, "//tbody/tr[1]/td[3]").text == name_of_beneficiary_on_table, self.logger.info(
                "**** TEST FAILED: BENEFICIARY'S ACCOUNT WAS NOT CREATED ***")
            self.logger.info("***** TEST PASSED: BENEFICIARY'S ACCOUNT WAS CREATED *****")

        except AssertionError:
            self.logger.error("Assertion Error: User's account was not created as expected.")
            raise

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

        finally:
            time.sleep(3)
            self.driver.quit()

    def test_the_deactivation_of_beneficiary(self, setup):
        """
        Test the deactivation and reactivation process of a beneficiary within the application.
        This includes verifying the status changes and appropriate alert messages upon state changes.
        """
        try:
            # Initialization: Setup test logging and open the website
            self.log_test_start("***** TEST THE DEACTIVATION OF A BENEFICIARY. *****")
            self.open_website_and_log_in_user(setup, self.URL)

            # Beneficiary Page Setup: Access beneficiary management and prepare for interaction
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)
            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()
            self.logger.info("***** USER IS NAVIGATED TO THE BENEFICIARY PAGE. *****")
            # Deactivation Process: Change beneficiary status to 'Inactive'
            self.Beneficiary_page_objects.change_the_status_of_beneficiary()

            # Final Status Validation: Ensure the beneficiary is marked as 'inactive'
            assert self.Beneficiary_page_objects.read_the_status_of_the_beneficiary() == "Inactive", (
                self.logger.info("**** TEST FAILED: BENEFICIARY'S ACCOUNT IS NOT DEACTIVATED ***")
            )
            self.logger.info("***** TEST PASSED: BENEFICIARY'S ACCOUNT IS DEACTIVATED  *****")
        except AssertionError:
            # Error Handling: Log assertion errors and raise them for further investigation
            self.logger.error("Assertion Error: AN ERROR OCCURRED ")
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
            self.log_test_start("***** TEST THE ACTIVATION OF A BENEFICIARY. *****")
            self.open_website_and_log_in_user(setup, self.URL)

            # Beneficiary Page Setup: Access beneficiary management and prepare for interaction
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)
            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()
            self.logger.info("***** USER SHOULD BE ON THE PAGE OF THE BENEFICIARIES *****")
            # Deactivation Process: Change beneficiary status to 'Inactive'
            self.Beneficiary_page_objects.change_the_status_of_beneficiary()
            time.sleep(4)

            # Validate Status: Ensure the beneficiary is marked as 'Active'
            assert self.Beneficiary_page_objects.read_the_status_of_the_beneficiary() == "Active", (
                self.logger.info("***** TEST FAILED: BENEFICIARY IS NOT ACTIVATED *****")
            )
            self.logger.info("***** TEST PASSED: BENEFICIARY IS ACTIVATED *****")

        except AssertionError:
            # Error Handling: Log assertion errors and raise them for further investigation
            self.logger.error("Assertion Error: ERROR OCCURRED.")
            raise

        except Exception as e:
            # Unexpected Error Handling: Log any unforeseen exceptions and raise them
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

        finally:
            # Cleanup: Ensure the browser session is properly closed, even if errors occur
            self.driver.quit()



