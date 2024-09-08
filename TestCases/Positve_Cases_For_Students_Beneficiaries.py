# Import necessary modules and classes
import random
import time
import requests
from Utilities import ReadXyfile
from selenium.webdriver.common.by import By
from Utilities.RecordLogger import RecordLogger
from Utilities.ReadProperties import ReadProperties
from PageObject.LoginObjects import LoginObjects
from PageObject.SignUpObjects import SignupObjects
from PageObject.BeneficiaryObject import BeneficiaryObjects

# to run the test use:   pytest -v -s TestCases/Negative_Login_Test_Case.py--browser chrome to run and also generate
# the html report use: pytest -v -s --html=Reports\reports.html TestCases/Positive_Login_Test_Case.py --browser chrome
"""
Test cases for the beneficiary page

Verify that a student can sign up as a beneficiary on the system (Check for the navigation when the user clicks on the student option)
Verify the response of the system when the student uses the same information for a student who is already on the database 
Verify the response of the system when all the filed are left empty 
Verify that a student can be activated and deactivated after creation (Check the message given by the system for this action)

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

    def est_that_a_student_can_become_beneficiary(self,setup):
        try:
            # Initialize Beneficiary page objects
            self.log_test_start("Test_that_a_student_can_become_beneficiary")
            self.open_website_and_log_in_user(setup, self.URL)
            self.logger.info("***** User is logged into account. *****")
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)
            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()
            time.sleep(3)
            self.Beneficiary_page_objects.click_on_the_new_beneficiary_button()
            time.sleep(3)
            self.logger.info("***** Clicking on the student option. *****")
            self.Beneficiary_page_objects.click_on_the_student_beneficiary_option()
            time.sleep(2)
            self.logger.info("***** User is navigated to the form for the creation a student beneficiary. *****")

            self.Beneficiary_page_objects.input_student_number(1)
            self.Beneficiary_page_objects.input_student_First_Name(SignupObjects.generate_names(self.driver))
            self.Beneficiary_page_objects.input_student_Last_Name(SignupObjects.generate_names(self.driver))
            self.Beneficiary_page_objects.input_student_phone_number(SignupObjects.generate_phone_number(self.driver))
            self.Beneficiary_page_objects.input_student_email(SignupObjects.email_generator(self.driver))
            Courses = ["Chemical Engineering", "Chemistry", "Fine Art"
                       "Biological Sciences", "Physics", "Mechanical Engineering"
                       "Adult Education", "Computer science", "Greek Language"]
            self.Beneficiary_page_objects.input_student_course(random.choice(Courses))
            self.Beneficiary_page_objects.Select_school()
            """
            The selection of the school is still pending. Get schools in the dropdown and proceed with the automation 
            """

            self.Beneficiary_page_objects.click_on_the_proceed_button()
        except AssertionError:
            self.logger.error("Assertion Error: this is not the page the user intends to go to.")
            raise
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise
        finally:
            self.driver.quit()

    def test_that_the_user_can_no_create_a_beneficiary_with_empty_fields(self, setup):
        try:
            # Initialize Beneficiary page objects
            self.log_test_start("***** Test that the user can no create a beneficiary with empty fields. *****")
            self.open_website_and_log_in_user(setup, self.URL)
            self.logger.info("***** User is logged into account. *****")
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)
            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()

            self.Beneficiary_page_objects.click_on_the_new_beneficiary_button()
            time.sleep(3)
            self.logger.info("***** Clicking on the student option. *****")
            self.Beneficiary_page_objects.click_on_the_student_beneficiary_option()
            time.sleep(2)
            self.logger.info("***** User is navigated to the form and fills nothing. *****")

            self.logger.info("***** User clicks on the proceed button *****")
            self.Beneficiary_page_objects.click_on_the_proceed_button()

            expected_message = "All fields are required"
            assert expected_message in self.driver.find_element(By.TAG_NAME, "body").text, self.logger.info(
                "**** TEST FAILED: USER'S ACCOUNT WAS NOT CREATED ***")
            self.logger.info("***** TEST PASSED: ERROR MESSAGE IS THROWN *****")

        except AssertionError:
            self.logger.error("Assertion Error: User's account was created.")
            raise

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

        finally:
            self.driver.quit()