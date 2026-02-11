import pytest
import time
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen

class Test_Login_Logout_Visible:
    home_url = "https://bridge-uat.nios.ac.in/"
    email = ReadConfig.getLoginEmail()
    password = ReadConfig.getLoginPassword()
    logger = LogGen.loggen()
    
    def test_login_logout_single_flow(self, setup):
        self.logger.info("**** Starting Visible Login-Logout Flow ****")
        self.driver = setup
        
        # FORCE WINDOW TO FRONT WITH ALERT
        self.driver.execute_script("alert('CHROME IS OPEN! Click OK to continue test.');")
        time.sleep(2)
        
        try:
            # Accept the alert
            alert = self.driver.switch_to.alert
            alert.accept()
        except:
            pass
        
        self.driver.get(self.home_url)
        
        # 1. Navigation Phase
        home_page = HomePage(self.driver)
        home_page.navigate_to_teacher_login()
        
        # 2. Login Phase
        login_page = LoginPage(self.driver)
        self.logger.info("=== PLEASE ENTER CAPTCHA ===")
        if not login_page.login_with_manual_captcha(self.email, self.password, timeout=300):
            pytest.fail("Login failed")
            
        self.logger.info("✅ Login successful. Waiting 5 seconds on Dashboard...")
        time.sleep(5)
        
        # 3. Logout Phase
        dashboard_page = DashboardPage(self.driver)
        
        self.logger.info("Opening User Dropdown...")
        dashboard_page.do_click(dashboard_page.dropdown_user)
        time.sleep(2)
        
        self.logger.info("Hovering over 'Logout' link...")
        dashboard_page.mouse_hover(dashboard_page.link_logout)
        time.sleep(3)  # Visual confirmation
        
        self.logger.info("Clicking Logout...")
        dashboard_page.do_click(dashboard_page.link_logout)
        
        # 4. Verification Phase
        time.sleep(5)
        current_url = self.driver.current_url
        self.logger.info(f"Current URL after logout: {current_url}")
        
        if "login" in current_url.lower() or "auth" in current_url.lower() or current_url == self.home_url:
            self.logger.info("✅ Logout Successful!")
            assert True
        else:
            self.logger.error(f"❌ Logout Failed: URL is {current_url}")
            assert False
            
        self.logger.info("**** Test Completed Successfully ****")
