import pytest
from selenium import webdriver
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

@pytest.fixture()
def setup(browser, headless):
    logger = LogGen.loggen()
    if browser == 'chrome':
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        logger.info("Launching Chrome browser")
    elif browser == 'firefox':
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
        logger.info("Launching Firefox browser")
    else:
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        logger.info("Launching Chrome browser as default")
        
    driver.implicitly_wait(ReadConfig.getImplicitWait())
    driver.maximize_window()
    yield driver
    driver.quit()

def pytest_addoption(parser):
    parser.addoption("--browser")
    parser.addoption("--headless", action="store_true", help="Run tests in headless mode")

@pytest.fixture()
def browser(request):
    return request.config.getoption("--browser")

@pytest.fixture()
def headless(request):
    return request.config.getoption("--headless")


