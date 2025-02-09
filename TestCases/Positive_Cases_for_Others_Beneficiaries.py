# Import necessary modules and classes
import random
import time
import requests
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.common.by import By
from Utilities.RecordLogger import RecordLogger
from Utilities.ReadProperties import ReadProperties

from PageObject.SignUpObjects import SignupObjects
from PageObject.BeneficiaryObject import BeneficiaryObjects
from selenium.webdriver.support import expected_conditions as ec

# to run the test use:   pytest -v -s TestCases/Negative_Cases_for_Login.py--browser chrome to run and also generate
# the html report use: pytest -v -s --html=Reports\reports.html TestCases/Positive_Cases_for_Login.py --browser chrome
"""
Test cases for the beneficiary page

Verify the response of the system when any of the fields are left empty 
Verify the deactivation of a other beneficiary 
Verify the activation of a other beneficiary

"""


class Test_Other_Beneficiary:
    # Initialize class variables with URLs, logger instance, and Excel file path
    URL = ReadProperties.getTestPageURL()  # Get main page URL from configuration
    # loginPageUrl = ReadProperties.LoginURL()  # Get login page URL from configuration
    User_email, UserPassword = ReadProperties.getUserDetails()
    EXISTING_EMAIL = User_email  # Get existing email from configuration
    EXISTING_PASSWORD = UserPassword  # Get existing password
    # from configuration
    logger = RecordLogger.log_generator_info()  # Initialize logger instance



    def test_the_functionality_of_the_beneficiary_navigation(self, setup, log_test_start, open_website_and_logging_user_in):
        try:
            # Initialize Beneficiary page objects
            log_test_start("***** TEST THE FUNCTIONALITY OF THE BENEFICIARY NAVIGATION *****")
            open_website_and_logging_user_in(self.URL)
            self.driver = setup
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)
            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()

            #waiting foe the table to be visible on the dashboard after clicking on the beneficiary option on the nav bar
            WebDriverWait(self.driver, timeout= 10).until(
                ec.presence_of_element_located((By.XPATH, "//div[1]/main[1]/div[1]/section[2]"))
            )

            self.logger.info("*****THE BENEFICIARY'S DATA LOGGING TABLE IS SEEN WITH ALL THE BENEFICIARY *****")
            button_locator = self.driver.find_element(By.XPATH, self.Beneficiary_page_objects.New_Beneficiary_xpath)


            assert "New Beneficiary" in button_locator.text.strip(), self.logger.info(
                "**** TEST FAILED: USER'S ACCOUNT WAS NOT CREATED ***")
            self.logger.info("***** TEST PASSED: NAVIGATION TO THE BENEFICIARY PAGE IS FUNCTIONAL *****")

            self.Beneficiary_page_objects.click_on_the_new_beneficiary_button()
            modal_name = "Select Beneficiary Type"
            assert modal_name in self.driver.find_element(By.TAG_NAME, "body").text, self.logger.info(
                "****TEST FAILED: THE MODAL WAS NOT FOUND FOR THE BENEFICIARY OPTIONS. ******")
            self.logger.info("*****TEST PASSED: THE MODAL WAS FOUND AND THE NAME WAS CORRECT.*****")

        except AssertionError:
            self.logger.error("Assertion Error: this is not the page the user intends to go to.")
            raise
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise
        finally:
            self.driver.quit()

    def test_verifying_the_form_navigation_from_the_modal(self, setup, open_website_and_logging_user_in, log_test_start):
        try:
            # Initialize Beneficiary page objects
            log_test_start("Test_the_functionality_of_the_others_beneficiary_navigation")
            open_website_and_logging_user_in(self.URL)
            self.driver = setup

            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)
            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()

            # waiting foe the table to be visible on the dashboard after clicking on the beneficiary option on the nav bar
            WebDriverWait(self.driver, timeout=10).until(
                ec.presence_of_element_located((By.XPATH, "//div[1]/main[1]/div[1]/section[2]"))
            )
            self.Beneficiary_page_objects.click_on_the_new_beneficiary_button()
            self.Beneficiary_page_objects.click_on_the_student_beneficiary_option()


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

    def est_the_creation_of_new_other_beneficiary(self, setup, log_test_start, open_website_and_logging_user_in):
        try:
            log_test_start("***** TESTING THE CREATION OF NEW OTHER BENEFICIARY.******")
            open_website_and_logging_user_in(self.URL)
            self.driver = setup

            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)

            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()
            time.sleep(3)
            self.Beneficiary_page_objects.click_on_the_new_beneficiary_button()
            self.Beneficiary_page_objects.click_on_the_student_beneficiary_option()
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

    def est_search_other_beneficiary_created(self, setup, log_test_start, open_website_and_logging_user_in):
        try:
            log_test_start("***** TESTING THE SEARCH FUNCTIONALITY ON OTHERS BENEFICIARY.******")
            open_website_and_logging_user_in(self.URL)
            self.driver = setup

            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)
            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()

            # Getting the name of a user that is on the table and searching for them
            names_of_all_beneficiary_on_table = self.Beneficiary_page_objects.Get_all_names_of_the_beneficiary()
            name_of_beneficiary_on_table = names_of_all_beneficiary_on_table[random.randint(1,10)]

            self.Beneficiary_page_objects.click_and_input_name_of_the_Beneficiary(name_of_beneficiary_on_table)

            assert name_of_beneficiary_on_table in self.driver.find_element(By.TAG_NAME, "body").text, self.logger.info("TEST FAILED: THE RESULT IS NOT CORRECT FOR THE SEARCHED PARAM")
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

    def est_the_deactivation_of_beneficiary(self, setup, log_test_start, open_website_and_logging_user_in):
        """
        Test the deactivation and reactivation process of a beneficiary within the application.
        This includes verifying the status changes and appropriate alert messages upon state changes.
        """
        try:
            # Initialization: Setup test logging and open the website
            log_test_start("***** TEST THE DEACTIVATION OF A BENEFICIARY. *****")
            open_website_and_logging_user_in(self.URL)
            self.driver = setup

            # Beneficiary Page Setup: Access beneficiary management and prepare for interaction
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)
            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()
            self.logger.info("***** USER IS NAVIGATED TO THE BENEFICIARY PAGE. *****")
            button_xpath = "//tbody/tr[1]/td[5]/button/span"

            # Check if the beneficiary is currently inactive
            if self.Beneficiary_page_objects.read_the_status_of_the_beneficiary() == "Inactive":
                # Validate that the button displays "Activate" when the user is inactive

                assert self.driver.find_element(By.XPATH, button_xpath).text.strip()== "Activate"

                # Deactivation Process: Attempt to change the status of the inactive beneficiary
                self.Beneficiary_page_objects.change_the_status_of_beneficiary()

                # Validate that the button text updates to "Deactivate" after activation
                Element_locator = self.driver.find_element(By.XPATH, button_xpath)
                self.Beneficiary_page_objects.wait_for_button_text_change("text", self.Beneficiary_page_objects.Status_action_button_xpath,"Deactivate")
                assert Element_locator.text.strip() == "Deactivate"

                # Verify that the status changes to "Active" after activation
                assert self.Beneficiary_page_objects.read_the_status_of_the_beneficiary() == "Active", (
                    self.logger.info("**** TEST FAILED: BENEFICIARY'S ACCOUNT IS NOT ACTIVATED ***")
                )
                self.logger.info("***** TEST PASSED: BENEFICIARY'S ACCOUNT IS ACTIVATED *****")

            # Check if the beneficiary is currently active
            elif self.Beneficiary_page_objects.read_the_status_of_the_beneficiary() == "Active":
                # Validate that the button displays "Deactivate" when the user is active
                assert self.driver.find_element(By.XPATH, button_xpath).text.strip()== "Deactivate"

                # Deactivation Process: Attempt to change the status of the active beneficiary
                self.Beneficiary_page_objects.change_the_status_of_beneficiary()

                # Validate that the button text updates to "Activate" after deactivation
                Element_locator = self.driver.find_element(By.XPATH, button_xpath)
                self.Beneficiary_page_objects.wait_for_button_text_change("text", self.Beneficiary_page_objects.Status_action_button_xpath, "Activate")
                assert Element_locator.text.strip() == "Activate"

                # Verify that the status changes to "Inactive" after deactivation
                assert self.Beneficiary_page_objects.read_the_status_of_the_beneficiary() == "Inactive", (
                    self.logger.info("**** TEST FAILED: BENEFICIARY'S ACCOUNT IS NOT DEACTIVATED ***")
                )
                self.logger.info("***** TEST PASSED: BENEFICIARY'S ACCOUNT IS DEACTIVATED *****")

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

    def est_verify_the_dashboard_for_Other_beneficiary(self, setup, log_test_start, open_website_and_logging_user_in):
        try:
            log_test_start("***** TESTING THE SEARCH FUNCTIONALITY ON OTHERS BENEFICIARY.******")
            open_website_and_logging_user_in(self.URL)
            self.driver = setup

            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)
            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()
            time.sleep(3)
            beneficiary = self.driver.find_element(By.XPATH, "//tbody/tr[1]/td[3]")
            time.sleep(4)
            Dashboard_name = beneficiary.text
            beneficiary.click()
            assert Dashboard_name == self.driver.find_element(By.XPATH, "//a[1]/h3[1]"), self.logger.infor("**** TEST FAILED: THE BOARD TITLE IS WRONG ****")
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









