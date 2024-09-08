# Import necessary modules and classes
import time
import requests

from selenium.webdriver.common.by import By
from Utilities.RecordLogger import RecordLogger
from PageObject.LoginObjects import LoginObjects
from Utilities.ReadProperties import ReadProperties



# to run the test use:   pytest -v -s TestCases/Positive_Cases_for_Login.py --browser chrome to run and also generate
# the html report use: pytest -v -s --html=Reports\reports.html TestCases/Positive_Cases_for_Login.py --browser chrome

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
    def open_website(self, setup, url):
        self.log_test_start("Open Website")
        self.driver = setup
        self.driver.get(url)
        self.driver.maximize_window()
        self.log_test_end("Open Website")

    # Test functionality of the signin link
    def test_functionality_of_the_signin_link_01_A(self, setup):
        self.log_test_start("**** For checking the title of the login page *****")
        self.open_website(setup, self.URL)
        self.LO = LoginObjects(self.driver)

        # Click on signin link
        self.LO.click_on_the_register_link()
        assert self.driver.title == "vnitpay", self.logger.info("*** TEST FAILED: THE PAGE PRESENTED ISN'T THE "
                                                                "LOGIN PAGE ****")
        self.logger.info("**** TEST PASSED: THE LOGIN PAGE WAS SHOWN *****")
        self.log_test_end("**** test_functionality_of_the_signin_link_010 *****")
        self.driver.quit()

    # Test valid login. Verify that a user can successfully log in with valid credentials and log out.

    def test_valid_login_001_B(self, setup):
        try:
            self.log_test_start("***** test_valid_login_011 *****")
            self.open_website(setup, self.URL)
            self.LO = LoginObjects(self.driver)
            self.logger.info("***** input the email and the password into the necessary fields *****")
            self.LO.input_email(self.EXISTING_EMAIL)
            self.LO.input_password(self.EXISTING_PASSWORD)
            self.logger.info("***** Click on the login button *****")
            self.LO.click_on_the_signin_button()
            time.sleep(4)
            self.logger.info("***** Collect the entire text of the page body and"
                             " check for the presence of the welcome message "
                             "*****")

            text_of_body = self.driver.find_element(By.TAG_NAME, "body").text

            assert "Hi, Bassey Jay 👋" in text_of_body, self.logger.info("*** TEST FAILED: LOGIN PROCESS FAILED ***")
            self.logger.info("*** TEST SUCCESSFUL: LOGIN PROCESS SUCCESSFUL ***")

            self.LO.click_on_the_logout_button()
            assert self.driver.title == "vnitpay", self.logger.info("*** TEST FAILED: THE PAGE PRESENTED ISN'T THE "
                                                                    "LOGIN PAGE ****")
            self.logger.info("**** TEST PASSED: LOGOUT PROCESS SUCCESSFUL *****")

        except AssertionError:
            self.logger.error("Assertion Error: Test condition failed.")
            raise  # Re-raise the exception to indicate test failure

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise  # Re-raise the exception to indicate test failure

        finally:
            self.log_test_end("******* test_valid_login_011*******")
            self.driver.quit()


    def test_All_Links_on_the_Homepage_Page_(self, setup):
        # Start the test and log the information
        try:
            self.logger.info("************** TEST START **************")
            self.logger.info("*************** Login Page Links Functionality Verification *********** ")

            # Initialize the WebDriver
            self.open_website(setup, self.ProductionURL)
            time.sleep(3)

            # Get all links on the page
            all_links = self.driver.find_elements(By.TAG_NAME, "a")
            self.logger.info(f"The total number of links on this page is {len(all_links)}")

            # Initialize counters for broken and functional links
            count_broken = 0
            count_functional = 0

            # Iterate through all links and check their status
            for link in all_links:
                url = link.get_attribute("href")
                try:
                    response = requests.head(url)
                except:
                    response = None

                if response is not None and response.status_code >= 400:
                    count_broken += 1
                    self.logger.info(f"THIS LINK {link} IS BROKEN")
                    print(f"THIS LINK {link} IS BROKEN")
                else:
                    count_functional += 1
                    self.logger.info(f"THIS LINK {link} IS FUNCTIONAL")
                    print(f"THIS LINK {link} IS FUNCTIONAL")

            # Log the total number of broken and functional links
            self.logger.info(f"TOTAL BROKEN LINKS: {count_broken}")
            self.logger.info(f"TOTAL FUNCTIONAL LINKS: {count_functional}")

            # Assert that there are no broken links
            assert count_broken == 0, "TEST FAILED: THERE ARE BROKEN LINKS ON THE PAGE"
            self.logger.info("TEST PASSED: ALL LINKS ARE FUNCTIONAL")

        except Exception as e:
            # Log any exceptions that occur during the test
            self.logger.error(f"Exception occurred: {str(e)}")
            assert False, f"Test failed due to exception: {str(e)}"
