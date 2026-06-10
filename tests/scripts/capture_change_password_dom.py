import pytest
import time
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen

class Test_008_ChangePasswordDOM:
    home_url = "https://bridge-uat.nios.ac.in/"
    email = ReadConfig.getLoginEmail()
    password = ReadConfig.getLoginPassword()
    logger = LogGen.loggen()
    
    def test_capture_change_password_dom(self, setup):
        self.driver = setup
        self.driver.get(self.home_url)
        
        home_page = HomePage(self.driver)
        home_page.navigate_to_teacher_login()
        
        login_page = LoginPage(self.driver)
        login_page.login_with_manual_captcha(self.email, self.password, timeout=120)
        
        # Navigate to Change Password
        dashboard_page = DashboardPage(self.driver)
        self.driver.get("https://bridge-uat.nios.ac.in/teacher/change-password")
        time.sleep(5)
        
        with open("change_password_dom.html", "w", encoding="utf-8") as f:
            f.write(self.driver.page_source)
        self.logger.info("Saved Change Password page DOM.")
