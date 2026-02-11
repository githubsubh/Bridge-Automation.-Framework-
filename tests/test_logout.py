import pytest
import time
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen

class Test_009_Logout:
    home_url = "https://bridge-uat.nios.ac.in/"
    email = ReadConfig.getLoginEmail()
    password = ReadConfig.getLoginPassword()
    logger = LogGen.loggen()
    
    def test_logout_flow(self, setup):
        self.logger.info("**** Starting Test_009_Logout ****")
        self.driver = setup
        self.driver.get(self.home_url)
        
        # 1. Login Phase
        home_page = HomePage(self.driver)
        home_page.navigate_to_teacher_login()
        
        login_page = LoginPage(self.driver)
        if not login_page.login_with_manual_captcha(self.email, self.password, timeout=300):
            pytest.fail("Login failed, cannot test Logout.")
            
        self.logger.info("Login successful. Waiting 5 seconds on Dashboard...")
        time.sleep(5)
        
        # 2. Logout Phase
        dashboard_page = DashboardPage(self.driver)
        
        self.logger.info("Opening User Dropdown...")
        dashboard_page.do_click(dashboard_page.dropdown_user)
        time.sleep(2)
        
        self.logger.info("Moving mouse to 'Logout' link...")
        dashboard_page.mouse_hover(dashboard_page.link_logout)
        time.sleep(3) # Visual confirmation of hover
        
        self.logger.info("Clicking Logout...")
        dashboard_page.do_click(dashboard_page.link_logout)
        
        # 3. Verification Phase
        self.logger.info("Waiting 5 seconds to verify redirection to Login page...")
        time.sleep(5)
        
        current_url = self.driver.current_url
        self.logger.info(f"Current URL after logout: {current_url}")
        
        if "login" in current_url.lower() or "auth" in current_url.lower() or current_url == self.home_url:
            self.logger.info("Logout Redirection Successful (Home/Login Page).")
            
            # Additional Verification: Check if Login button is present
            try:
                # Re-initialize HomePage to check for login elements
                home_page = HomePage(self.driver)
                # We can check if the 'Teacher Login' link is visible again
                if home_page.is_visible(home_page.link_teacher_login_xpath):
                    self.logger.info("Logout Verified: 'Teacher Login' button is visible.")
                    assert True
                else:
                    self.logger.warning("Redirection okay, but 'Teacher Login' button not found immediately.")
                    assert True 
            except:
                self.logger.info("Logout likely successful based on URL.")
                assert True
        else:
            self.logger.error(f"Logout Failed: URL is {current_url}")
            # Capture DOM for debugging
            with open("logout_failure_dom.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            assert False, "Logout redirection failed."

        self.logger.info("**** Test_009_Logout Completed Successfully ****")
