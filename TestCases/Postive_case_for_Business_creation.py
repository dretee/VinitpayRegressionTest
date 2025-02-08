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
Test cases for the adding a business to the system 

Verify that the user can add a business and make the user a merchant
Verify that the user can accept vouchers after becoming a business 

"""

class Test_Business_positive_test_cases:
    # Initialize class variables with URLs, logger instance, and Excel file path
    URL = ReadProperties.getTestPageURL()  # Get main page URL from configuration
    # loginPageUrl = ReadProperties.LoginURL()  # Get login page URL from configuration
    User_email, UserPassword = ReadProperties.getUserDetails()
    EXISTING_EMAIL = User_email  # Get existing email from configuration
    EXISTING_PASSWORD = UserPassword  # Get existing password
    # from configuration
    logger = RecordLogger.log_generator_info()  # Initialize logger instance

    # initialize the  name of the business
    name_Of_created_business = None


    """
    Test the creation of all kind of business in the system. There are 12 kinds and they can be opened in all states  in nigeria
    """
    test_data = [
        (1, "Gas Station", 1),
        (2, "Super Market", 2),
        (3, "Air Line", 3),
        (4, "Mechanic Workshop", 4),
        (5, "Towing Vehicle", 5),
        (6, "University", 6),
        (7, "School", 7),
        (8, "Restaurant", 8),
        (9, "Agro Vendor", 9),
        (10, "Car Park", 10),
        (11, "Others", 11)
    ]

    @pytest.mark.parametrize("number_associated_with_business, Type_of_business, State_located", test_data)
    def  test_verify_that_a_new_business_can_be_created(self, setup, open_website_and_logging_user_in, log_test_end, number_associated_with_business, Type_of_business, State_located):
        try:
            open_website_and_logging_user_in(self.URL)
            self.driver = setup
            self.Business_Objects = BusinessObjects(self.driver)
            self.Business_Objects.locate_and_click_username_and_add_business_button()

            # Assert that the navigation to a modal is correct
            modal_header = "Hi, Let's setup your business"
            assert modal_header == self.driver.find_element(By.XPATH, self.Business_Objects.business_creation_modal_message_xpath).text, self.logger.info("**** TEST FAILED: THE NAVIGATION WAS WRONG")
            self.logger.info("*****TEST PASSED: THE MODAL TITLE IS CORRECT*****")

            Test_Business_positive_test_cases.name_Of_created_business = self.Business_Objects.locate_and_input_business_name()


            self.Business_Objects.input_the_description_text(
                f"This is a {Type_of_business} business. And will be using Vnitpay business feature for its day to day tracking")

            self.Business_Objects.select_a_category_from_all_the_options(number_associated_with_business)

            self.Business_Objects.click_on_the_next_button()

            # next modal to complete the creation

            self.Business_Objects.select_a_country_from_all_the_options()
            self.Business_Objects.select_a_province_from_all_the_options(State_located)
            self.Business_Objects.input_the_address_of_the_user("NO 6 Adewunmi close Agbara estate")
            self.Business_Objects.click_on_the_create_business_button()
            time.sleep(5)
            body_text = self.driver.find_element(By.TAG_NAME, "body").text

            assert Test_Business_positive_test_cases.name_Of_created_business  in body_text,  self.logger.info("**** TEST FAILED: THE BUSINESS WAS NOT CREATED.*****")
            self.logger.info("*****TEST PASSED: THE BUSINESS WAS CREATED AND THE USER GOT THE SUCCESS MESSAGE POP UP*****")

        except AssertionError:
            self.logger.error("Assertion Error: this is not the page the user intends to go to.")
            raise
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise
        finally:
            self.driver.quit()


    # Checking that the business was created and can be searched for on the business list on the application
    def test_searching_for_newly_created_business(self,setup, open_website_and_logging_user_in, log_test_start):
        log_test_start("VERIFY THAT THE USER CAN SEARCH ON THE BUSINESS THEY WANT FROM THE MERCHANT SEARCH BAR")
        open_website_and_logging_user_in(self.URL)
        self.driver = setup
        self.Business_Objects = BusinessObjects(self.driver)
        result_of_search = self.Business_Objects.input_name_into_the_search_field(Test_Business_positive_test_cases.name_Of_created_business)

        assert result_of_search == Test_Business_positive_test_cases.name_Of_created_business, self.logger.info("**** TEST FAILED: BUSINESS WAS NOT FOUND")
        self.logger.info("*****TEST PASSED: BUSINESS WAS FOUND. *****")






