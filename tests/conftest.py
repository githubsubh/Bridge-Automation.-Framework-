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
        
        import os
        import time
        pwd = os.getcwd()
        profile_path = os.path.join(pwd, "automation_profiles", f"profile_{int(time.time())}")
        if not os.path.exists(profile_path):
            os.makedirs(profile_path, exist_ok=True)
            
        options.add_argument(f"--user-data-dir={profile_path}")
        options.add_argument("--profile-directory=Default")
        
        # Essential flags to avoid first-run popups and background tasks
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-first-run")
        options.add_argument("--no-default-browser-check")
        options.add_argument("--password-store=basic")
        options.add_argument("--start-maximized")

        logger.info(f"Initializing isolated Chrome session with profile: {profile_path}")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.maximize_window()
        # Ensure it comes to front
        try:
            driver.set_window_position(0, 0)
            driver.execute_script("window.focus();")
        except:
            pass
        logger.info("Launching isolated Chrome browser")
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


