import pytest
import time
from pages.home_page import HomePage
from pages.login_page import LoginPage
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen

class Test_Analyze_Dashboard:
    home_url = "https://bridge-uat.nios.ac.in/"
    email = ReadConfig.getLoginEmail()
    password = ReadConfig.getLoginPassword()
    logger = LogGen.loggen()
    
    def test_capture_dashboard_analysis(self, setup):
        self.logger.info("**** Analyzing Dashboard for remaining automation ****")
        self.driver = setup
        self.driver.get(self.home_url)
        
        home_page = HomePage(self.driver)
        home_page.navigate_to_teacher_login()
        
        login_page = LoginPage(self.driver)
        if not login_page.login_with_manual_captcha(self.email, self.password, timeout=120):
            pytest.fail("Login failed.")
            
        time.sleep(5)
        
        # Capture the full DOM of the dashboard for detailed analysis
        with open("dashboard_analysis_live.html", "w", encoding="utf-8") as f:
            f.write(self.driver.page_source)
        
        self.logger.info("Dashboard DOM saved for analysis. Look for unaddressed sections.")
        time.sleep(5)
