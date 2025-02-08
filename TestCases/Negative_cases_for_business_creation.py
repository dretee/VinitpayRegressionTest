# Import necessary modules and classes
import time

import pytest
from selenium.webdriver.common.by import By

from Utilities.RecordLogger import RecordLogger
from Utilities.ReadProperties import ReadProperties
from PageObject.BusinessObjects import BusinessObjects


# to run the test use:   pytest -v -s TestCases/Negative_Login_Test_Case.py--browser chrome to run and also generate
# the html report use: pytest -v -s --html=Reports\reports.html TestCases/Positive_Login_Test_Case.py --browser chrome
"""
Test cases for the business creation

Verify the response of the system when the user tries creating the business with empty field 
Verify the response of the system with all the field been empty and the creation process is initiated 
Verify that the input data type for the business field can only allow names and not numbers and special characters
Verify that the input data type for the description field can only allow not numbers and special characters
Verify that the 
"""

class Test_Login:
    # Initialize class variables with URLs, logger instance, and Excel file path
    URL = ReadProperties.getTestPageURL()  # Get main page URL from configuration
    # loginPageUrl = ReadProperties.LoginURL()  # Get login page URL from configuration
    User_email, UserPassword = ReadProperties.getUserDetails()
    # from configuration
    logger = RecordLogger.log_generator_info()  # Initialize logger instance


    # input fields business names, categories and Descriptions for the first modal of  business creation
    test_data = [
        ("", "3", "This is a business", "Please enter valid company name and description"), # Missing business name
        ("Homeies dapping", "3", "", "Please enter valid company name and description"),
        ("", "4", "", "Please enter valid company name and description"), # Missing business name and description

    ]
    @pytest.mark.parametrize("business_name, category, description, error_message", test_data)
    def test_verify_that_the_user_get_a_correct_error_message_with_empty_fields(self, setup, business_name, log_test_start, open_website_and_logging_user_in, category, description, error_message ):
        try:
            log_test_start("")
            open_website_and_logging_user_in(self.URL)
            self.driver = setup
            self.Business_Objects = BusinessObjects(self.driver)
            self.Business_Objects.locate_and_click_username_and_add_business_button()

            self.driver.find_element(By.XPATH, "//form/div[1]/div/input").send_keys(business_name)
            self.Business_Objects.input_the_description_text(description)
            self.Business_Objects.select_a_category_from_all_the_options(category)
            self.Business_Objects.click_on_the_next_button()

            error_message_text = self.driver.find_element(By.XPATH, "//div[@class='error-div']").text

            assert error_message == error_message_text, self.logger.info("**** TEST FAILED: ERROR MESSAGE IS WRONG ******")
            self.logger.info("*** TEST PASSED: ERROR MESSAGE IS CORRECT ****")

        except AssertionError:
            self.logger.error("Assertion Error: this is not the page the user intends to go to.")
            raise
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise
        finally:
            self.driver.quit()


    test_data = [
    ("Homeies dapping", "This is a business", "Please select a business category"),  # Missing category
    ("", "This is a business", "Please enter valid company name and description"),  # Missing business name and description
    ("", "", "Please enter valid company name and description"),  # Missing category
    ("Homeies dapping", "", "Please enter valid company name and description") # Missing category and description
    ]

    @pytest.mark.parametrize("business_name, description, error_message", test_data)
    def est_verify_that_the_category_field_when_missing_the_correct_error_message_is_given(self,setup, log_test_start, open_website_and_logging_user_in,business_name, description, error_message):
        try:
            log_test_start("")
            open_website_and_logging_user_in(self.URL)
            self.driver = setup
            self.Business_Objects = BusinessObjects(self.driver)
            self.Business_Objects.locate_and_click_username_and_add_business_button()

            self.driver.find_element(By.XPATH, "//form/div[1]/div/input").send_keys(business_name)
            self.Business_Objects.input_the_description_text(description)

            self.Business_Objects.click_on_the_next_button()

            error_message_text = self.driver.find_element(By.XPATH, "//div[@class='error-div']").text

            assert error_message == error_message_text, self.logger.info("**** TEST FAILED: ERROR MESSAGE IS WRONG ******")
            self.logger.info("*** TEST PASSED: ERROR MESSAGE IS CORRECT ****")

        except AssertionError:
            self.logger.error("Assertion Error: this is not the page the user intends to go to.")
            raise
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise
        finally:
            self.driver.quit()

