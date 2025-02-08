# Import necessary modules and classes
import random
import time

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


class Test_Student_Beneficiary_Positive_Tests:
    # Initialize class variables with URLs, logger instance, and Excel file path
    URL = ReadProperties.getTestPageURL()  # Get main page URL from configuration
    # loginPageUrl = ReadProperties.LoginURL()  # Get login page URL from configuration
    User_email, UserPassword = ReadProperties.getUserDetails()
    # from configuration
    logger = RecordLogger.log_generator_info()  # Initialize logger instance

    Names = None


    def test_that_a_student_can_become_beneficiary(self,setup,open_website_and_logging_user_in, log_test_start):
        try:
            # Initialize Beneficiary page objects
            log_test_start("Test_that_a_student_can_become_beneficiary")
            open_website_and_logging_user_in(self.URL)
            self.driver = setup
            self.logger.info("***** User is logged into account. *****")
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)
            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()

            self.Beneficiary_page_objects.click_on_the_new_beneficiary_button()
            time.sleep(3)
            self.Beneficiary_page_objects.click_on_the_student_beneficiary_option()

            time.sleep(2)
            self.logger.info("***** User is navigated to the form for the creation a student beneficiary. *****")

            self.Beneficiary_page_objects.input_student_number(1001)

            # Generate the Names and make the list global to be used for the search
            self.Signup_Object = SignupObjects.generate_names(self.driver)
            First_name, Last_name = self.Signup_Object.generate_names()
            Test_Student_Beneficiary_Positive_Tests.Names = [First_name, Last_name]

            self.Beneficiary_page_objects.input_student_First_Name(First_name)
            self.Beneficiary_page_objects.input_student_Last_Name(Last_name)
            self.Beneficiary_page_objects.input_student_phone_number( self.Signup_Object.generate_phone_number(self.driver))
            self.Beneficiary_page_objects.input_student_email( self.Signup_Object.email_generator(self.driver))
            Courses = ["Chemical Engineering", "Chemistry", "Fine Art"
                       "Biological Sciences", "Physics", "Mechanical Engineering"
                       "Adult Education", "Computer science", "Greek Language"]
            self.Beneficiary_page_objects.input_student_course(random.choice(Courses))
            self.Beneficiary_page_objects.Select_school()
            """
            The selection of the school is still pending. Get schools in the dropdown and proceed with the automation 
            """
            self.Beneficiary_page_objects.click_on_the_proceed_button()

            beneficiary = self.driver.find_element(By.XPATH, "//tbody/tr[1]/td[3]")

            # Check that the name on the board is correct with that which was used to create it
            assert f"{First_name} {Last_name}" in beneficiary.text, self.logger.infor(
                "**** TEST FAILED: THE STUDENT WAS NOT CREATED****")
            self.logger.info("**** TEST PASSED:THE STUDENT WAS CREATED.****")


        except AssertionError:
            self.logger.error("Assertion Error: this is not the page the user intends to go to.")
            raise
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise
        finally:
            self.driver.quit()

    def test_verify_the_dashboard_for_Student_beneficiary(self, setup, log_test_start,open_website_and_logging_user_in):
            try:
                log_test_start("***** TESTING THE SEARCH FUNCTIONALITY ON OTHERS BENEFICIARY.******")
                open_website_and_logging_user_in(self.URL)
                self.driver = setup
                self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)
                self.Beneficiary_page_objects.click_on_the_Beneficiary_option()
                beneficiary = self.driver.find_element(By.XPATH, "//tbody/tr[1]/td[3]")
                beneficiary.click()

                # Check that once the user clicks on the created beneficiary the name on the board is correct and agings with that which was used to create them
                assert beneficiary.text in self.driver.find_element(By.XPATH, "//a[1]/h3[1]"), self.logger.infor("**** TEST FAILED: THE BOARD TITLE IS WRONG ****")
                self.logger.info("**** TEST PASSED: BOARD TITLE IS CORRECT.****")

            except AssertionError:
                self.logger.error("Assertion Error: User's account was not created as expected.")
                raise

            except Exception as e:
                self.logger.error(f"An unexpected error occurred: {e}")
                raise

            finally:
                time.sleep(3)
                self.driver.quit()

    def test_search_student_beneficiary_created(self, setup, log_test_start, open_website_and_logging_user_in):
        try:
            log_test_start("***** TESTING THE SEARCH FUNCTIONALITY ON STUDENT BENEFICIARY.******")
            open_website_and_logging_user_in(self.URL)
            self.driver = setup
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)
            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()

            #Get the student first and last name from the list which was created when the student was created
            First_name, Last_name = Test_Student_Beneficiary_Positive_Tests.Names
            name_of_students = f"{First_name} {Last_name}"
            self.Beneficiary_page_objects.click_and_input_name_of_the_Beneficiary(name_of_students)
            time.sleep(3)

            name_on_the_search_result = self.driver.find_element(By.XPATH, "//tbody/tr[1]/td[3]").text

            assert name_of_students in name_on_the_search_result, self.logger.info(
                "TEST FAILED: THE RESULT IS NOT CORRECT FOR THE SEARCHED PARAM")
            self.logger.info("****TEST PASSED: RESULT OF THE SEARCH WAS CORRECT****")

        except AssertionError:
            self.logger.error("Assertion Error: User's account was not created as expected.")
            raise

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

        finally:
            time.sleep(3)
            self.driver.quit()

    def test_the_deactivation_of_beneficiary(self, setup, open_website_and_logging_user_in, log_test_start):
        """
        Test the deactivation and reactivation process of a beneficiary within the application.
        This includes verifying the status changes and appropriate alert messages upon state changes.
        """
        try:
            log_test_start("***** TESTING THE SEARCH FUNCTIONALITY ON STUDENT BENEFICIARY.******")
            open_website_and_logging_user_in(self.URL)
            self.driver = setup
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)
            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()

            #Get the student first and last name from the list which was created when the student was created
            First_name, Last_name = Test_Student_Beneficiary_Positive_Tests.Names
            name_of_students = f"{First_name} {Last_name}"
            self.Beneficiary_page_objects.click_and_input_name_of_the_Beneficiary(name_of_students)
            time.sleep(3)

            self.logger.info("***** USER IS NAVIGATED TO THE BENEFICIARY PAGE. *****")
            # Deactivation Process: Change beneficiary status to 'inactive'
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

    def test_the_activation_of_beneficiary(self, setup, open_website_and_logging_user_in, log_test_start):
        """
        Test the deactivation and reactivation process of a beneficiary within the application.
        This includes verifying the status changes and appropriate alert messages upon state changes.
        """
        try:
            self.log_test_start("***** TESTING THE SEARCH FUNCTIONALITY ON STUDENT BENEFICIARY.******")
            open_website_and_logging_user_in(self.URL)
            self.driver = setup
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)
            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()

            # Get the student first and last name from the list which was created when the student was created
            First_name, Last_name = Test_Student_Beneficiary_Positive_Tests.Names
            name_of_students = f"{First_name} {Last_name}"
            self.Beneficiary_page_objects.click_and_input_name_of_the_Beneficiary(name_of_students)
            time.sleep(3)

            self.logger.info("***** USER SHOULD BE ON THE PAGE OF THE BENEFICIARIES *****")
            # Activation Process: Change beneficiary status to 'active'
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

