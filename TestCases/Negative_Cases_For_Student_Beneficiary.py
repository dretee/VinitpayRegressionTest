# Import necessary modules and classes
import random
import time

import pytest

from selenium.webdriver.common.by import By

from TestCases.conftest import setup, open_website_and_logging_user_in, log_test_start
from Utilities.RecordLogger import RecordLogger
from Utilities.ReadProperties import ReadProperties

from PageObject.SignUpObjects import SignupObjects
from PageObject.BeneficiaryObject import BeneficiaryObjects

# to run the test use:   pytest -v -s TestCases/Negative_Login_Test_Case.py--browser chrome to run and also generate
# the html report use: pytest -v -s --html=Reports\reports.html TestCases/Positive_Login_Test_Case.py --browser chrome
"""
Test cases for the beneficiary page

Verify the response of the system when on of the fields are left empty and the suer tries to proceed to a creation 

"""

#@pytest.mark.usefixtures(setup, open_website_and_logging_user_in, log_test_start)
class Test_Student_Beneficiary_Negative_Tests:
    # Initialize class variables with URLs, logger instance, and Excel file path
    URL = ReadProperties.getTestPageURL()  # Get main page URL from configuration
    # loginPageUrl = ReadProperties.LoginURL()  # Get login page URL from configuration
    User_email, UserPassword = ReadProperties.getUserDetails()
    EXISTING_EMAIL = User_email  # Get existing email from configuration
    EXISTING_PASSWORD = UserPassword  # Get existing password
    # from configuration
    logger = RecordLogger.log_generator_info()  # Initialize logger instance


    def est_creation_of_new_student_beneficiary_without_course(self, setup, open_website_and_logging_user_in, log_test_start):
        """Test the creation of a new beneficiary without filling the required fields."""
        try:
            log_test_start("***** TESTING THE CREATION OF NEW STUDENT BENEFICIARY WITH MISSING COURSE FILED. ******")
            open_website_and_logging_user_in(self.URL)
            self.driver = setup
            # Initialize Beneficiary page objects
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)

            # Navigate to beneficiary creation page
            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()
            time.sleep(2)
            self.Beneficiary_page_objects.click_on_the_new_beneficiary_button()

            self.Beneficiary_page_objects.click_on_the_student_beneficiary_option()
            self.logger.info("***** User is navigated to the form for the creation a student beneficiary. *****")

            self.Beneficiary_page_objects.input_student_number(1)
            self.Beneficiary_page_objects.input_student_phone_number(SignupObjects.generate_phone_number(self.driver))
            self.Beneficiary_page_objects.input_student_First_Name(SignupObjects.generate_names(self.driver))
            self.Beneficiary_page_objects.input_student_Last_Name(SignupObjects.generate_names(self.driver))
            self.Beneficiary_page_objects.input_student_email(SignupObjects.email_generator(self.driver))

            self.logger.info("***** USER INPUTS THE THE COURSE IN THE CORRECT FIELD.******")
            Courses = ["Chemical Engineering", "Chemistry", "Fine Art"
                       "Biological Sciences", "Physics", "Mechanical Engineering",
                       "Computer science", "Greek Language"]
            self.Beneficiary_page_objects.input_student_course(random.choice(Courses))

            self.logger.info("***** User clicks on the proceed button *****")
            self.Beneficiary_page_objects.click_on_the_proceed_button()
            time.sleep(2)

            assert "All fields are required" in self.driver.find_element(By.TAG_NAME, "body").text, self.logger.info(
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

    test_data = [
        (" "," ", " ", " ", " ", " ", "All fields are required"),  # all fields empty
        ("", "Mark", "Mark", "0801234543", "markhommie@gmail.com", "Chemical Engineering", "All fields are required"),# Empty student number
        ("1212","", "Mark", "0801234543", "markhommie@gmail.com", "Chemical Engineering", "All fields are required"),  # Empty first name
        ("1212","Mark", "", "0801234543", "markhommie@gmail.com", "Physics", "All fields are required"),  # Empty last name
        ("1212","Mark", "Mark", "", "markhommie@gmail.com", "English", "All fields are required"),  # Empty phone number
        ("1212","Mark", "Mark", "0801234543", "", "Hydrogen Engineering", "All fields are required"),  # Empty email
        ("1212","Mark", "Mark", "0801234543", "markhommie@gmail.com", "", "All fields are required"),  # Empty course
        ("1212","Mark", "Mark", "0801234543", "markhommie@gmail.com", "123456", "All fields are required"),  # Invalid course (use a number for this)
        ("1212","Mark", "Mark", "0801234543", "markhommie@gmail.com", "123456", "All fields are required")  # Invalid student number
    ]

    @pytest.mark.parametrize("Student_number, Firstname, Lastname, Phone_number, Email, course, error_message", test_data)
    def test_the_creation_of_new_other_beneficiary_with_missing_fields(self, setup, open_website_and_logging_user_in, log_test_start, Student_number, Firstname, Lastname, Phone_number,
                                                                       Email, course,  error_message):
        try:
            log_test_start("***** TESTING THE CREATION OF NEW OTHER BENEFICIARY.******")
            open_website_and_logging_user_in(self.URL)
            self.driver = setup
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)

            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()
            time.sleep(2)
            self.Beneficiary_page_objects.click_on_the_new_beneficiary_button()
            self.Beneficiary_page_objects.click_on_the_student_beneficiary_option()


            # This is to fill the form
            self.Beneficiary_page_objects.input_student_number(Student_number)
            self.Beneficiary_page_objects.input_phone_number(Phone_number)
            self.Beneficiary_page_objects.input_first_name(Firstname)
            self.Beneficiary_page_objects.input_last_name(Lastname)
            self.Beneficiary_page_objects.input_email(Email)
            self.Beneficiary_page_objects.input_student_course(course)

            self.logger.info("***** USER SELECTS THE THE SCHOOL IN THE CORRECT FIELD.******")
            self.Beneficiary_page_objects.Select_school()

            self.logger.info("***** USER CLICKS ON THE PROCEED BUTTON.******")
            self.Beneficiary_page_objects.click_on_the_proceed_button()

            assert error_message == self.driver.find_element(By.XPATH,
                                                             "//div[@class='error-div']").text, self.logger.info(
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


    """
        Test to check that invalid first name can not be used for the creation of a student account
        First name invalid data test for the creation of the student ["12345", "@JaneDoe"]    
    """


    test_data = [
        ("1212", "12345", "Mark", "0801234543", "markhommie@gmail.com", "Hydrogen Engineering", "First name format is invalid"),  # Invalid first name
        ("1212", "@JaneDoe", "Mark", "0801234543", "markhommie@gmail.com", "Hydrogen Engineering", "First name format is invalid"),  # Invalid first name
    ]

    @pytest.mark.parametrize("Student_number, Firstname, Lastname, Phone_number, Email, course, error_message", test_data)
    def est_creation_of_student_beneficiary_with_invalid_data_in_all_first_name_fields(self, setup, open_website_and_logging_user_in, log_test_start, Student_number, Firstname, Lastname, Phone_number,
                                                                       Email, course,  error_message):
        try:
            log_test_start("***** TESTING THE CREATION OF NEW OTHER BENEFICIARY.******")
            open_website_and_logging_user_in(setup, self.URL)
            self.driver = setup
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)

            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()
            time.sleep(2)
            self.Beneficiary_page_objects.click_on_the_new_beneficiary_button()
            self.Beneficiary_page_objects.click_on_the_student_beneficiary_option()

            # This is to fill the form
            self.Beneficiary_page_objects.input_student_number(Student_number)
            self.Beneficiary_page_objects.input_phone_number(Phone_number)
            self.Beneficiary_page_objects.input_first_name(Firstname)
            self.Beneficiary_page_objects.input_last_name(Lastname)
            self.Beneficiary_page_objects.input_email(Email)
            self.Beneficiary_page_objects.input_student_course(course)

            self.logger.info("***** USER SELECTS THE THE SCHOOL IN THE CORRECT FIELD.******")
            self.Beneficiary_page_objects.Select_school()

            self.logger.info("***** USER CLICKS ON THE PROCEED BUTTON.******")
            self.Beneficiary_page_objects.click_on_the_proceed_button()

            assert error_message == self.driver.find_element(By.XPATH,
                                                             "//div[@class='error-div']").text, self.logger.info(
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
        # firstname invalid data test for the creation of the student ["12345", "@JaneDoe"]

    """
        Test to check that invalid last name can not be used for the creation of a student account
    """
    test_data = [
        ("1212", "Mark", "12345", "0801234543", "markhommie@gmail.com", "Hydrogen Engineering", "Last name format is invalid"),# Invalid first name
        ("1212", "Mark", "@Doe", "0801234543", "markhommie@gmail.com", "Hydrogen Engineering","Last name format is invalid"),  # Invalid first name
    ]

    @pytest.mark.parametarized("Student_number, Firstname, Lastname, Phone_number, Email, course, error_message", test_data)
    def est_creation_of_student_beneficiary_with_invalid_data_in_all_last_name_fields(self, setup, open_website_and_logging_user_in, log_test_start, Student_number, Firstname,
                                                                                        Lastname, Phone_number,
                                                                                        Email, course, error_message):
        try:
            log_test_start("***** TESTING THE CREATION OF NEW STUDENT BENEFICIARY WITH INVALID DATA.******")
            open_website_and_logging_user_in(setup, self.URL)
            self.driver = setup
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)

            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()
            time.sleep(2)
            self.Beneficiary_page_objects.click_on_the_new_beneficiary_button()
            self.Beneficiary_page_objects.click_on_the_student_beneficiary_option()

            # This is to fill the form
            self.Beneficiary_page_objects.input_student_number(Student_number)
            self.Beneficiary_page_objects.input_phone_number(Phone_number)
            self.Beneficiary_page_objects.input_first_name(Firstname)
            self.Beneficiary_page_objects.input_last_name(Lastname)
            self.Beneficiary_page_objects.input_email(Email)
            self.Beneficiary_page_objects.input_student_course(course)

            self.logger.info("***** USER SELECTS THE THE SCHOOL IN THE CORRECT FIELD.******")
            self.Beneficiary_page_objects.Select_school()

            self.logger.info("***** USER CLICKS ON THE PROCEED BUTTON.******")
            self.Beneficiary_page_objects.click_on_the_proceed_button()

            assert error_message == self.driver.find_element(By.XPATH,
                                                             "//div[@class='error-div']").text, self.logger.info(
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

    """
        Test to check that invalid phone number can not be used for the creation of a student account
    """
    test_data = [
        ("1212", "Mark", "Mark", "12345", "markhommie@gmail.com", "Hydrogen Engineering", "Phone number format is invalid"),
        # Invalid phone number
        ("1212", "Mark", "Mark", "phone123", "markhommie@gmail.com", "Hydrogen Engineering", "Phone number format is invalid"),
        # Invalid phone number
        ("1212", "Mark", "Mark", "@12345", "markhommie@gmail.com", "Hydrogen Engineering", "Phone number format is invalid"),
        # Invalid phone number
    ]

    @pytest.mark.parametrize("Student_number, Firstname, Lastname, Phone_number, Email, course, error_message", test_data)
    def est_creation_of_student_beneficiary_with_invalid_data_in_all_phone_number_fields(self, setup, open_website_and_logging_user_in, log_test_start,  Student_number, Firstname,
                                                                                       Lastname, Phone_number,
                                                                                       Email, course, error_message):
        try:
            log_test_start("***** TESTING THE CREATION OF NEW STUDENT BENEFICIARY WITH INVALID DATA.******")
            open_website_and_logging_user_in(self.URL)
            self.driver = setup
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)

            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()
            time.sleep(2)
            self.Beneficiary_page_objects.click_on_the_new_beneficiary_button()
            self.Beneficiary_page_objects.click_on_the_student_beneficiary_option()

            # This is to fill the form
            self.Beneficiary_page_objects.input_student_number(Student_number)
            self.Beneficiary_page_objects.input_phone_number(Phone_number)
            self.Beneficiary_page_objects.input_first_name(Firstname)
            self.Beneficiary_page_objects.input_last_name(Lastname)
            self.Beneficiary_page_objects.input_email(Email)
            self.Beneficiary_page_objects.input_student_course(course)

            self.logger.info("***** USER SELECTS THE THE SCHOOL IN THE CORRECT FIELD.******")
            self.Beneficiary_page_objects.Select_school()

            self.logger.info("***** USER CLICKS ON THE PROCEED BUTTON.******")
            self.Beneficiary_page_objects.click_on_the_proceed_button()

            assert error_message == self.driver.find_element(By.XPATH,
                                                             "//div[@class='error-div']").text, self.logger.info(
                "**** TEST FAILED: BENEFICIARY'S ACCOUNT WAS NOT CREATED ***")
            self.logger.info("***** TEST PASSED: BENEFICIARY'S ACCOUNT WAS CREATED *****")

        except AssertionError:
            self.logger.error("Assertion Error: User's account was created.")
            raise

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

        finally:
            time.sleep(3)
            self.driver.quit()



    """
    Test to check that invalid email can not be used for the creation of a student account
    """
    test_data = [
        ("1212", "Mark", "Mark", "0801234543", "user@.com", "Hydrogen Engineering", "Phone number format is invalid"),
        # Invalid phone number
        ("1212", "Mark", "Mark", "0801234543", "user@domain", "Hydrogen Engineering", "Phone number format is invalid"),
        # Invalid phone number
    ]

    @pytest.mark.parametrize("Student_number, Firstname, Lastname, Phone_number, Email, course, error_message", test_data)
    def est_creation_of_student_beneficiary_with_invalid_data_in_all_email_fields(self, setup, open_website_and_logging_user_in, log_test_start, Student_number, Firstname,
                                                                                       Lastname, Phone_number,
                                                                                       Email, course, error_message):
        try:
            log_test_start("***** TESTING THE CREATION OF NEW STUDENT BENEFICIARY WITH INVALID DATA.******")
            open_website_and_logging_user_in(self.URL)
            self.driver = setup
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)

            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()
            time.sleep(2)
            self.Beneficiary_page_objects.click_on_the_new_beneficiary_button()
            self.Beneficiary_page_objects.click_on_the_student_beneficiary_option()

            # This is to fill the form
            self.Beneficiary_page_objects.input_student_number(Student_number)
            self.Beneficiary_page_objects.input_phone_number(Phone_number)
            self.Beneficiary_page_objects.input_first_name(Firstname)
            self.Beneficiary_page_objects.input_last_name(Lastname)
            self.Beneficiary_page_objects.input_email(Email)
            self.Beneficiary_page_objects.input_student_course(course)

            self.logger.info("***** USER SELECTS THE THE SCHOOL IN THE CORRECT FIELD.******")
            self.Beneficiary_page_objects.Select_school()

            self.logger.info("***** USER CLICKS ON THE PROCEED BUTTON.******")
            self.Beneficiary_page_objects.click_on_the_proceed_button()

            assert error_message == self.driver.find_element(By.XPATH,
                                                             "//div[@class='error-div']").text, self.logger.info(
                "**** TEST FAILED: BENEFICIARY'S ACCOUNT WAS NOT CREATED ***")
            self.logger.info("***** TEST PASSED: BENEFICIARY'S ACCOUNT WAS CREATED *****")

        except AssertionError:
            self.logger.error("Assertion Error: User's account was created.")
            raise

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

        finally:
            time.sleep(3)
            self.driver.quit()

    """
        Test to check that invalid email can not be used for the creation of a student account
        """
    test_data = [
        ("12345!", "Mark", "Mark", "0801234543", "markhommie@gmail.com", "Hydrogen Engineering", "Phone number format is invalid"),
        # Invalid phone number
        ("12@345", "Mark", "Mark", "0801234543", "markhommie@gmail.com", "Hydrogen Engineering", "Phone number format is invalid"),
        # Invalid phone number
    ]

    @pytest.mark.parametrize("Student_number, Firstname, Lastname, Phone_number, Email, course, error_message",
                               test_data)
    def est_creation_of_student_beneficiary_with_invalid_data_in_all_email_fields(self, setup, open_website_and_logging_user_in, log_test_start, Student_number,
                                                                                   Firstname,
                                                                                   Lastname, Phone_number,
                                                                                   Email, course, error_message):
        try:
            log_test_start("***** TESTING THE CREATION OF NEW STUDENT BENEFICIARY WITH INVALID DATA.******")
            open_website_and_logging_user_in(self.URL)
            self.driver = setup
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)

            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()
            time.sleep(2)
            self.Beneficiary_page_objects.click_on_the_new_beneficiary_button()
            self.Beneficiary_page_objects.click_on_the_student_beneficiary_option()

            # This is to fill the form
            self.Beneficiary_page_objects.input_student_number(Student_number)
            self.Beneficiary_page_objects.input_phone_number(Phone_number)
            self.Beneficiary_page_objects.input_first_name(Firstname)
            self.Beneficiary_page_objects.input_last_name(Lastname)
            self.Beneficiary_page_objects.input_email(Email)
            self.Beneficiary_page_objects.input_student_course(course)

            self.logger.info("***** USER SELECTS THE THE SCHOOL IN THE CORRECT FIELD.******")
            self.Beneficiary_page_objects.Select_school()

            self.logger.info("***** USER CLICKS ON THE PROCEED BUTTON.******")
            self.Beneficiary_page_objects.click_on_the_proceed_button()

            assert error_message == self.driver.find_element(By.XPATH,
                                                             "//div[@class='error-div']").text, self.logger.info(
                "**** TEST FAILED: BENEFICIARY'S ACCOUNT WAS NOT CREATED ***")
            self.logger.info("***** TEST PASSED: BENEFICIARY'S ACCOUNT WAS CREATED *****")

        except AssertionError:
            self.logger.error("Assertion Error: User's account was created.")
            raise

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

        finally:
            self.driver.quit()