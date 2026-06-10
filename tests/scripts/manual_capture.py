import pytest
import time
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen

class Test_Manual_Capture:
    home_url = "https://bridge-uat.nios.ac.in/"
    email = ReadConfig.getLoginEmail()
    password = ReadConfig.getLoginPassword()
    logger = LogGen.loggen()
    
    def test_manual_nav_capture(self, setup):
        self.driver = setup
        self.driver.get(self.home_url)
        
        home_page = HomePage(self.driver)
        home_page.navigate_to_teacher_login()
        
        login_page = LoginPage(self.driver)
        if not login_page.login_with_manual_captcha(self.email, self.password, timeout=120):
            pytest.fail("Login failed.")
            
        time.sleep(5)
        
        # Manual jump to payment history
        self.logger.info("Jumping to /transactions...")
        self.driver.get(self.home_url + "transactions")
        time.sleep(10)
        
        with open("payment_history_live.html", "w", encoding="utf-8") as f:
            f.write(self.driver.page_source)
        self.logger.info("Payment History DOM saved.")
