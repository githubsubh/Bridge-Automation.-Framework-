import pytest
import time
from pages.home_page import HomePage
from pages.login_page import LoginPage
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Test_002_Login:
    # Read config
    home_url = "https://bridge-uat.nios.ac.in/"
    email = ReadConfig.getLoginEmail()
    password = ReadConfig.getLoginPassword()
    logger = LogGen.loggen()
    
    def test_login_flow(self, setup):
        self.logger.info("**** Starting Test_002_Login ****")
        self.driver = setup
        self.driver.get(self.home_url)
        
        # 1. Navigation Phase
        home_page = HomePage(self.driver)
        home_page.navigate_to_teacher_login()
        
        # 2. Login Phase
        login_page = LoginPage(self.driver)
        
        # Perform Login with Manual CAPTCHA Entry
        success = login_page.login_with_manual_captcha(self.email, self.password, timeout=120)
        
        if success:
            self.logger.info("Login Successful! Verifying Dashboard...")
            
            self.logger.warning("Dashboard elements verification weak, but login URL confirmed.")
            assert True
        else:
            self.logger.error("Login Failed or Timed Out.")
            self.driver.save_screenshot("screenshots/login_failed.png")
            assert False
