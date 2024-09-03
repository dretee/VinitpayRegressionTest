# Import necessary modules and classes
import time
import requests

from PageObject.BeneficiaryObject import BeneficiaryObjects
from PageObject.SignUpObjects import SignupObjects
from Utilities import ReadXyfile
from selenium.webdriver.common.by import By
from Utilities.RecordLogger import RecordLogger
from Utilities.ReadProperties import ReadProperties
from PageObject.LoginObjects import LoginObjects

# to run the test use:   pytest -v -s TestCases/invalidLoginTestCase.py--browser chrome to run and also generate
# the html report use: pytest -v -s --html=Reports\reports.html TestCases/validLoginTestCase.py --browser chrome
"""
Negative test cases for the Other beneficiary creation

Verify the response of the system when a url, name and special characters are inputted in the phone number filed and other vaild data
Verify the response of the system when a url, email,  numbers and special characters (name with special characters) are inputted in the firstname and lastname filed and other vaild data
Verify the response of the system when a url, numbers and special characters (name with special characters) are inputted in the email filed and other vaild data


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

    def test_creation_of_new_other_beneficiary_filling_phone_number_fields(self, setup):
        """Test the creation of a new beneficiary without filling the required fields."""
        try:
            self.log_test_start("***** TESTING THE CREATION OF NEW BENEFICIARY WITH MISSING FILED. ******")
            self.open_website_and_log_in_user(setup, self.URL)

            # Initialize Beneficiary page objects
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)

            # Navigate to beneficiary creation page

            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()
            time.sleep(3)
            self.Beneficiary_page_objects.click_on_the_new_beneficiary_button()
            time.sleep(3)
            self.Beneficiary_page_objects.click_on_the_other_beneficiary_option()

            self.logger.info("***** USER SHOULD BE IN THE OTHER BENEFICIARY FORM *****")

            self.Beneficiary_page_objects.input_phone_number("08065748322")

            self.Beneficiary_page_objects.click_on_the_proceed_button()
            self.logger.info("***** USER HAS CLICKED ON THE PROCEED BUTTON *****")
            # Test various scenarios of field completion
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

    def test_creation_of_new_other_beneficiary_filling_First_Name_fields(self, setup):
        """Test the creation of a new beneficiary without filling the required fields."""
        try:
            self.log_test_start("***** TESTING THE CREATION OF NEW BENEFICIARY WITH MISSING FILED. ******")
            self.open_website_and_log_in_user(setup, self.URL)

            # Initialize Beneficiary page objects
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)

            # Navigate to beneficiary creation page
            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()
            time.sleep(3)
            self.Beneficiary_page_objects.click_on_the_new_beneficiary_button()
            time.sleep(3)
            self.Beneficiary_page_objects.click_on_the_other_beneficiary_option()

            self.logger.info("***** USER SHOULD BE IN THE OTHER BENEFICIARY FORM *****")
            First_name, _ = SignupObjects(self.driver).generate_names()
            self.Beneficiary_page_objects.input_first_name(First_name)

            self.Beneficiary_page_objects.click_on_the_proceed_button()
            self.logger.info("***** USER SHOULD HAVE CLICKED ON THE PROCEED BUTTON*****")
            # Test various scenarios of field completion
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

    def test_creation_of_new_other_beneficiary_filling_Last_Name_fields(self, setup):
        """Test the creation of a new beneficiary without filling the required fields."""
        try:
            self.log_test_start("***** TESTING THE CREATION OF NEW BENEFICIARY WITH MISSING FILED. ******")
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
            self.logger.info("***** THE LAST NAME FIELD SHOULD HAVE BEEN FILLED *****")

            self.Beneficiary_page_objects.click_on_the_proceed_button()
            self.logger.info("***** THE PROCEED BUTTON SHOULD HAVE BEEN CLICKED  *****")
            # Test various scenarios of field completion
            expected_message = "All fields are required"
            assert expected_message in self.driver.find_element(By.TAG_NAME, "body").text, self.logger.info(
                "**** TEST FAILED: USER'S ACCOUNT WAS CREATED ***")
            self.logger.info("***** TEST PASSED: ERROR MESSAGE IS THROWN *****")

        except AssertionError:
            self.logger.error("Assertion Error: User's account was created.")
            raise

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

        finally:
            self.driver.quit()

    def test_creation_of_new_other_beneficiary_filling_email_fields(self, setup):
        """Test the creation of a new beneficiary without filling the required fields."""
        try:
            self.log_test_start("***** TESTING THE CREATION OF NEW BENEFICIARY WITH MISSING FILED.******")
            self.open_website_and_log_in_user(setup, self.URL)

            # Initialize Beneficiary page objects
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)

            # Navigate to beneficiary creation page
            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()
            time.sleep(3)
            self.Beneficiary_page_objects.click_on_the_new_beneficiary_button()
            self.Beneficiary_page_objects.click_on_the_other_beneficiary_option()

            self.Beneficiary_page_objects.input_email(SignupObjects(self.driver).email_generator())
            self.logger.info("***** ONLY THE EMAIL HAS BEEN INPUTTED IN TO THE FIELD *****")
            time.sleep(3)
            self.Beneficiary_page_objects.click_on_the_proceed_button()
            self.logger.info("***** USER HAS CLICKED THE PROCEED BUTTON *****")
            # Test various scenarios of field completion
            expected_message = "All fields are required"
            assert expected_message in self.driver.find_element(By.TAG_NAME, "body").text, self.logger.info(
                "**** TEST FAILED: USER'S ACCOUNT WAS NOT CREATED ***")
            self.logger.info("***** TEST PASSED: ERROR MESSAGE IS THROWN TO THE USER *****")

        except AssertionError:
            self.logger.error("Assertion Error: User's account was created.")
            raise

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

        finally:
            self.driver.quit()

    def test_the_use_of_wrong_text_format_for_phone_number_field(self, setup):
        try:
            self.log_test_start(
                "***** TEST THE RESPONSE OF THE SYSTEM TO AN INVALID FORMAT INPUT IN THE PHONE NUMBER FIELD. *****")
            self.open_website_and_log_in_user(setup, self.URL)
            self.open_website_and_log_in_user(setup, self.URL)
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)

            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()
            time.sleep(3)
            self.Beneficiary_page_objects.click_on_the_new_beneficiary_button()
            self.Beneficiary_page_objects.click_on_the_other_beneficiary_option()

            First_name, Last_name = SignupObjects(self.driver).generate_names()
            self.Beneficiary_page_objects.input_first_name(First_name)
            self.log_test_start("***** USER INPUTS THE THE FIRST NAME IN THE CORRECT FIELD.******")
            time.sleep(3)
            self.Beneficiary_page_objects.input_last_name(Last_name)
            self.log_test_start("***** USER INPUTS THE THE LAST NAME IN THE CORRECT FIELD.******")

            self.Beneficiary_page_objects.input_email(SignupObjects(self.driver).email_generator())
            self.log_test_start("***** USER INPUTS THE THE EMAIL IN THE CORRECT FIELD.******")

            # The list consist of words, special character + numbers, URL and an incomplete number
            List_of_inputs = ["Housing", "???334%%%", "htpps://bscscan.com", "08098"]
            Number_of_inputs = len(List_of_inputs)
            Error_message_list = []

            for n in range(Number_of_inputs):
                time.sleep(2)
                self.Beneficiary_page_objects.input_phone_number(List_of_inputs[n])
                self.Beneficiary_page_objects.click_on_the_proceed_button()
                self.log_test_start("User clicks on the proceed button.")

                Body_text = self.driver.find_element(By.TAG_NAME, "Body").text
                error_detected = "Only digits are allowed in this field" in Body_text
                Error_message_list.append(error_detected)

            if all(Error_message_list):
                self.logger.info("Test passed: Error message is correctly thrown for all inputs.")
            else:
                self.logger.error("Test failed: Not all inputs triggered the correct error message.")
                raise AssertionError("User's account was created for an invalid input.")

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

        finally:
            self.driver.quit()

    def test_the_use_of_wrong_text_format_for_email_field(self, setup):
        try:
            self.log_test_start(
                "***** TEST THE RESPONSE OF THE SYSTEM TO AN INVALID FORMAT INPUT IN THE EMAIL FIELD. *****")
            self.open_website_and_log_in_user(setup, self.URL)
            self.open_website_and_log_in_user(setup, self.URL)
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)

            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()
            time.sleep(3)
            self.Beneficiary_page_objects.click_on_the_new_beneficiary_button()
            self.Beneficiary_page_objects.click_on_the_other_beneficiary_option()

            phone_number = SignupObjects(self.driver).generate_phone_number()
            self.Beneficiary_page_objects.input_phone_number(phone_number)
            self.log_test_start("***** USER INPUTS THE THE PHONE NUMBER IN THE CORRECT FIELD.******")

            First_name, Last_name = SignupObjects(self.driver).generate_names()
            self.Beneficiary_page_objects.input_first_name(First_name)
            self.log_test_start("***** USER INPUTS THE THE FIRST NAME IN THE CORRECT FIELD.******")
            time.sleep(3)
            self.Beneficiary_page_objects.input_last_name(Last_name)
            self.log_test_start("***** USER INPUTS THE THE LAST NAME IN THE CORRECT FIELD.******")

            # The list consist of words, special character + numbers, URL and an incomplete number
            List_of_inputs = ["Housing", "???334%%%", "htpps://bscscan.com", "08098"]
            Number_of_inputs = len(List_of_inputs)
            Error_message_list = []

            for n in range(Number_of_inputs):
                self.Beneficiary_page_objects.input_email(List_of_inputs[n])
                self.log_test_start("***** USER INPUTS THE THE INVALID DATA FORMAT IN THE EMAIL FIELD.******")

                self.Beneficiary_page_objects.click_on_the_proceed_button()
                self.log_test_start("***** USER CLICKS ON THE PROCEED BUTTON.******")

                Body_text = self.driver.find_element(By.TAG_NAME, "Body").text
                error_detected = "Only digits are allowed in this field" in Body_text
                Error_message_list.append(error_detected)

            if all(Error_message_list):
                self.logger.info("Test passed: Error message is correctly thrown for all inputs and beneficiafy are not created.")
            else:
                self.logger.error("Test failed: Not all inputs triggered the correct error message and beneficiary was created.")
                raise AssertionError("User's account was created for an invalid input.")

        except AssertionError:
            self.logger.error("Assertion Error: User's account was created.")
            raise

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

        finally:
            self.driver.quit()

    def test_the_use_of_wrong_text_format_for_email_field(self, setup):
        try:
            self.log_test_start(
                "***** TEST THE RESPONSE OF THE SYSTEM TO AN INVALID FORMAT INPUT IN THE PHONE NUMBER FIELD. *****")
            self.open_website_and_log_in_user(setup, self.URL)
            self.open_website_and_log_in_user(setup, self.URL)
            self.Beneficiary_page_objects = BeneficiaryObjects(self.driver)

            self.Beneficiary_page_objects.click_on_the_Beneficiary_option()
            time.sleep(3)
            self.Beneficiary_page_objects.click_on_the_new_beneficiary_button()
            self.Beneficiary_page_objects.click_on_the_other_beneficiary_option()

            phone_number = SignupObjects(self.driver).generate_phone_number()
            self.Beneficiary_page_objects.input_phone_number(phone_number)

            First_name, Last_name = SignupObjects(self.driver).generate_names()
            self.Beneficiary_page_objects.input_first_name(First_name)
            self.log_test_start("***** USER INPUTS THE THE FIRST NAME IN THE CORRECT FIELD.******")
            time.sleep(3)
            self.Beneficiary_page_objects.input_last_name(Last_name)
            self.log_test_start("***** USER INPUTS THE THE LAST NAME IN THE CORRECT FIELD.******")

            # The list consist of words, special character + numbers, URL and an incomplete number
            List_of_inputs = ["Housing", "???334%%%", "htpps://bscscan.com", "08098"]
            Number_of_inputs = len(List_of_inputs)

            for n in range(Number_of_inputs):
                self.Beneficiary_page_objects.input_email(List_of_inputs[n])
                self.log_test_start("***** USER INPUTS THE THE EMAIL IN THE CORRECT FIELD.******")

                self.Beneficiary_page_objects.click_on_the_proceed_button()
                self.log_test_start("***** USER CLICKS ON THE PROCEED BUTTON.******")

                """
                      complete this code
                """
        except AssertionError:
            self.logger.error("Assertion Error: User's account was created.")
            raise

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

        finally:
            self.driver.quit()
