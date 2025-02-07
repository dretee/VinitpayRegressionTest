import pytest
from selenium import webdriver
from Utilities.RecordLogger import RecordLogger
from Utilities.ReadProperties import ReadProperties

logger = RecordLogger.log_generator_info()  # Initialize logger instance


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

    return driver


def pytest_addoption(parser):
    parser.addoption("--browser")


@pytest.fixture()
def browser(request):
    return request.config.getoption("--browser")


@pytest.fixture()
def log_test_start():
    def _log_test(test_name):
        logger.info(f"****** STARTING TEST: {test_name} ******")
    return _log_test


@pytest.fixture()
def log_test_end():
    def _log_test(test_name):
        logger.info(f"****** ENDING TEST: {test_name} ******")
    return _log_test


@pytest.fixture()
def open_website(setup, log_test_start):
    def _open_website(url):
        log_start = log_test_start  # Get fixture return value

        log_start("Open Test")
        driver = setup
        driver.get(url)
        driver.maximize_window()

    return _open_website

