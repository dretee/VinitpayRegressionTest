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

Verify the response of the system when on of the fields are left empty and the suer tries to proceed to a creation 

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

    def test_creation_of_new_student_beneficiary_without_phone_number_(self, setup):
        """Test the creation of a new beneficiary without filling the required fields."""
        try:
            self.log_test_start("***** TESTING THE CREATION OF NEW STUDENT BENEFICIARY WITH MISSING PHONE NUMBER FILED. ******")
            self.open_website_and_log_in_user(setup, self.URL)

            # Initialize Beneficiary page objects
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)

            # Navigate to beneficiary creation page

            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()
            time.sleep(2)
            self.Beneficiary_page_objects.click_on_the_new_beneficiary_button()
            time.sleep(3)
            self.Beneficiary_page_objects.click_on_the_student_beneficiary_option()
            self.logger.info("***** User is navigated to the form for the creation a student beneficiary. *****")

            self.Beneficiary_page_objects.input_student_number(1)
            self.Beneficiary_page_objects.input_student_First_Name(SignupObjects.generate_names(self.driver))
            self.Beneficiary_page_objects.input_student_Last_Name(SignupObjects.generate_names(self.driver))
            self.Beneficiary_page_objects.input_student_email(SignupObjects.email_generator(self.driver))
            Courses = ["Chemical Engineering", "Chemistry", "Fine Art"
                       "Biological Sciences", "Physics", "Mechanical Engineering"
                       "Adult Education","Computer science", "Greek Language"]
            self.Beneficiary_page_objects.input_student_course(random.choice(Courses))

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

    def test_creation_of_new_student_beneficiary_without_first_name(self, setup):
        """Test the creation of a new beneficiary without filling the required fields."""
        try:
            self.log_test_start("***** TESTING THE CREATION OF NEW STUDENT BENEFICIARY WITH MISSING FIRST NAME FILED. ******")
            self.open_website_and_log_in_user(setup, self.URL)

            # Initialize Beneficiary page objects
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)

            # Navigate to beneficiary creation page

            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()
            time.sleep(2)
            self.Beneficiary_page_objects.click_on_the_new_beneficiary_button()
            time.sleep(3)
            self.Beneficiary_page_objects.click_on_the_student_beneficiary_option()
            time.sleep(2)
            self.logger.info("***** User is navigated to the form for the creation a student beneficiary. *****")

            self.Beneficiary_page_objects.input_student_number(1)
            self.Beneficiary_page_objects.input_student_phone_number(SignupObjects.generate_phone_number(self.driver))
            self.Beneficiary_page_objects.input_student_Last_Name(SignupObjects.generate_names(self.driver))
            self.Beneficiary_page_objects.input_student_email(SignupObjects.email_generator(self.driver))
            Courses = ["Chemical Engineering", "Chemistry", "Fine Art"
                       "Biological Sciences", "Physics", "Mechanical Engineering"
                       "Adult Education", "Computer science", "Greek Language"]
            self.Beneficiary_page_objects.input_student_course(random.choice(Courses))

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

    def test_creation_of_new_student_beneficiary_without_last_name(self, setup):
        """Test the creation of a new beneficiary without filling the required fields."""
        try:
            self.log_test_start("***** TESTING THE CREATION OF NEW STUDENT BENEFICIARY WITH MISSING LAST NAME FILED. ******")
            self.open_website_and_log_in_user(setup, self.URL)

            # Initialize Beneficiary page objects
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)

            # Navigate to beneficiary creation page

            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()
            time.sleep(2)
            self.Beneficiary_page_objects.click_on_the_new_beneficiary_button()
            time.sleep(3)
            self.Beneficiary_page_objects.click_on_the_student_beneficiary_option()
            time.sleep(2)
            self.logger.info("***** User is navigated to the form for the creation a student beneficiary. *****")

            self.Beneficiary_page_objects.input_student_number(1)
            self.Beneficiary_page_objects.input_student_phone_number(SignupObjects.generate_phone_number(self.driver))
            self.Beneficiary_page_objects.input_student_First_Name(SignupObjects.generate_names(self.driver))
            self.Beneficiary_page_objects.input_student_email(SignupObjects.email_generator(self.driver))
            Courses = ["Chemical Engineering", "Chemistry", "Fine Art"
                       "Biological Sciences", "Physics", "Mechanical Engineering"
                       "Adult Education","Computer science", "Greek Language"]
            self.Beneficiary_page_objects.input_student_course(random.choice(Courses))

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

    def test_creation_of_new_student_beneficiary_without_student_number(self, setup):
        """Test the creation of a new beneficiary without filling the required fields."""
        try:
            self.log_test_start("***** TESTING THE CREATION OF NEW STUDENT BENEFICIARY WITH MISSING STUDENT NUMBER FILED. ******")
            self.open_website_and_log_in_user(setup, self.URL)

            # Initialize Beneficiary page objects
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)

            # Navigate to beneficiary creation page

            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()
            time.sleep(2)
            self.Beneficiary_page_objects.click_on_the_new_beneficiary_button()
            time.sleep(3)
            self.Beneficiary_page_objects.click_on_the_student_beneficiary_option()
            time.sleep(2)
            self.logger.info("***** User is navigated to the form for the creation a student beneficiary. *****")

            self.Beneficiary_page_objects.input_student_Last_Name(SignupObjects.generate_names(self.driver))
            self.Beneficiary_page_objects.input_student_phone_number(SignupObjects.generate_phone_number(self.driver))
            self.Beneficiary_page_objects.input_student_First_Name(SignupObjects.generate_names(self.driver))
            self.Beneficiary_page_objects.input_student_email(SignupObjects.email_generator(self.driver))
            Courses = ["Chemical Engineering", "Chemistry", "Fine Art"
                       "Biological Sciences", "Physics", "Mechanical Engineering"
                       "Adult Education","Computer science", "Greek Language"]
            self.Beneficiary_page_objects.input_student_course(random.choice(Courses))

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

    def test_creation_of_new_student_beneficiary_without_email(self, setup):
        """Test the creation of a new beneficiary without filling the required fields."""
        try:
            self.log_test_start("***** TESTING THE CREATION OF NEW STUDENT BENEFICIARY WITH MISSING EMAIL FILED. ******")
            self.open_website_and_log_in_user(setup, self.URL)

            # Initialize Beneficiary page objects
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)

            # Navigate to beneficiary creation page

            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()
            time.sleep(2)
            self.Beneficiary_page_objects.click_on_the_new_beneficiary_button()
            time.sleep(3)
            self.Beneficiary_page_objects.click_on_the_student_beneficiary_option()
            time.sleep(2)
            self.logger.info("***** User is navigated to the form for the creation a student beneficiary. *****")

            self.Beneficiary_page_objects.input_student_number(1)
            self.Beneficiary_page_objects.input_student_Last_Name(SignupObjects.generate_names(self.driver))
            self.Beneficiary_page_objects.input_student_phone_number(SignupObjects.generate_phone_number(self.driver))
            self.Beneficiary_page_objects.input_student_First_Name(SignupObjects.generate_names(self.driver))

            Courses = ["Chemical Engineering", "Chemistry", "Fine Art"
                       "Biological Sciences", "Physics", "Mechanical Engineering"
                       "Adult Education","Computer science", "Greek Language"]
            self.Beneficiary_page_objects.input_student_course(random.choice(Courses))

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

    def test_creation_of_new_student_beneficiary_without_course(self, setup):
        """Test the creation of a new beneficiary without filling the required fields."""
        try:
            self.log_test_start("***** TESTING THE CREATION OF NEW STUDENT BENEFICIARY WITH MISSING COURSE FILED. ******")
            self.open_website_and_log_in_user(setup, self.URL)

            # Initialize Beneficiary page objects
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)

            # Navigate to beneficiary creation page

            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()
            time.sleep(2)
            self.Beneficiary_page_objects.click_on_the_new_beneficiary_button()
            time.sleep(3)
            self.Beneficiary_page_objects.click_on_the_student_beneficiary_option()
            time.sleep(2)
            self.logger.info("***** User is navigated to the form for the creation a student beneficiary. *****")

            self.Beneficiary_page_objects.input_student_number(1)
            self.Beneficiary_page_objects.input_student_phone_number(SignupObjects.generate_phone_number(self.driver))
            self.Beneficiary_page_objects.input_student_First_Name(SignupObjects.generate_names(self.driver))
            self.Beneficiary_page_objects.input_student_Last_Name(SignupObjects.generate_names(self.driver))
            self.Beneficiary_page_objects.input_student_email(SignupObjects.email_generator(self.driver))

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