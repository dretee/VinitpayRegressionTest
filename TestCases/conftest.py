import pytest
from selenium import webdriver

from PageObject.LoginObjects import LoginObjects
from Utilities.RecordLogger import RecordLogger
from Utilities.ReadProperties import ReadProperties

logger = RecordLogger.log_generator_info()  # Initialize logger instance
User_email, UserPassword = ReadProperties.getUserDetails()
EXISTING_EMAIL = User_email  # Get existing email from configuration
EXISTING_PASSWORD = UserPassword  # Get existing password



@pytest.fixture()
def open_website(setup, log_test_start):
    def _open_website(url):
        log_start = log_test_start  # Get fixture return value

        log_start("Open Test")
        driver = setup
        driver.get(url)
        driver.maximize_window()

    yield _open_website

@pytest.fixture()
def open_website_and_logging_user_in(setup):
    def _open_website_and_log_in_user(url):
        driver = setup
        driver.get(url)
        driver.maximize_window()
        Login_page_objects = LoginObjects(driver)

        # Log in user into their account
        Login_page_objects.input_email(EXISTING_EMAIL)
        Login_page_objects.input_password(EXISTING_PASSWORD)
        Login_page_objects.click_on_the_signin_button()

    yield _open_website_and_log_in_user


@pytest.fixture()
def setup(browser):
    if browser == "chrome":
        driver = webdriver.Chrome()
    elif browser == "firefox":
        driver = webdriver.Firefox()
    elif browser == "safari":
        driver = webdriver.Safari()
    elif browser == "edge":
        driver = webdriver.Edge()
    else:
        driver = webdriver.Chrome()

    yield driver

    driver.quit()


def pytest_addoption(parser):
    parser.addoption("--browser")


@pytest.fixture()
def browser(request):
    return request.config.getoption("--browser")


@pytest.fixture()
def log_test_start():
    def _log_test(test_name):
        logger.info(f"****** STARTING TEST: {test_name} ******")
    yield _log_test


@pytest.fixture()
def log_test_end():
    def _log_test(test_name):
        logger.info(f"****** ENDING TEST: {test_name} ******")
    yield _log_test

