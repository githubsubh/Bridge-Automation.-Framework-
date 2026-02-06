import pytest
import time
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen

class Test_Explore_EServices:
    home_url = "https://bridge-uat.nios.ac.in/"
    email = ReadConfig.getLoginEmail()
    password = ReadConfig.getLoginPassword()
    logger = LogGen.loggen()
    
    def test_explore_eservices_flow(self, setup):
        self.logger.info("**** Exploring E-Services for automation ****")
        self.driver = setup
        self.driver.get(self.home_url)
        
        home_page = HomePage(self.driver)
        home_page.navigate_to_teacher_login()
        
        login_page = LoginPage(self.driver)
        if not login_page.login_with_manual_captcha(self.email, self.password, timeout=120):
            pytest.fail("Login failed.")
            
        time.sleep(5)
        dashboard_page = DashboardPage(self.driver)
        
        # Navigate to E-Services Apply
        self.logger.info("Navigating to E-Services Apply...")
        dashboard_page.do_click(dashboard_page.link_eservices_apply)
        time.sleep(5)
        with open("eservices_apply_live.html", "w", encoding="utf-8") as f:
            f.write(self.driver.page_source)
        self.logger.info("E-Services Apply DOM saved.")
        
        # Go back to dashboard to navigate to My Requests
        self.driver.get(self.home_url + "teacher/dashboard")
        time.sleep(3)
        
        self.logger.info("Navigating to E-Services My Requests...")
        dashboard_page.do_click(dashboard_page.link_eservices_requests)
        time.sleep(5)
        with open("eservices_requests_live.html", "w", encoding="utf-8") as f:
            f.write(self.driver.page_source)
        self.logger.info("E-Services Requests DOM saved.")

        # Navigate to Payment History while we are at it
        self.driver.get(self.home_url + "teacher/dashboard")
        time.sleep(3)
        self.logger.info("Navigating to Payment History...")
        dashboard_page.do_click(dashboard_page.link_payment_history)
        time.sleep(5)
        with open("payment_history_live.html", "w", encoding="utf-8") as f:
            f.write(self.driver.page_source)
        self.logger.info("Payment History DOM saved.")
