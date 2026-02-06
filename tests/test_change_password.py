import pytest
import time
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.change_password_page import ChangePasswordPage
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen

class Test_008_ChangePassword:
    home_url = "https://bridge-uat.nios.ac.in/"
    email = ReadConfig.getLoginEmail()
    password = ReadConfig.getLoginPassword()
    logger = LogGen.loggen()
    
    def test_change_password_flow(self, setup):
        self.logger.info("**** Starting Test_008_ChangePassword ****")
        self.driver = setup
        self.driver.get(self.home_url)
        
        # 1. Login
        home_page = HomePage(self.driver)
        home_page.navigate_to_teacher_login()
        
        login_page = LoginPage(self.driver)
        if not login_page.login_with_manual_captcha(self.email, self.password, timeout=120):
            pytest.fail("Login failed, cannot test Change Password.")
            
        self.logger.info("Login successful. Waiting 5 seconds on Dashboard...")
        time.sleep(5)
        
        dashboard_page = DashboardPage(self.driver)
        
        # 2. Navigate to Change Password via Dropdown
        self.logger.info("--- Navigating to Change Password ---")
        self.logger.info("Clicking User Dropdown...")
        dashboard_page.do_click(dashboard_page.dropdown_user)
        time.sleep(1)
        
        self.logger.info("Moving mouse to 'Change Password' link...")
        dashboard_page.mouse_hover(dashboard_page.link_change_password)
        time.sleep(2) # Show the hover intent
        
        dashboard_page.do_click(dashboard_page.link_change_password)
        self.logger.info("Clicked Change Password. Waiting 5 seconds for page load...")
        time.sleep(5)
        
        # 3. Fill Change Password Form (Negative Attempt: New same as Current)
        cp_page = ChangePasswordPage(self.driver)
        
        self.logger.info("--- Phase 1: Negative Testing (Same as Current) ---")
        self.logger.info("Entering Current Password: Password@1")
        cp_page.enter_current_password("Password@1")
        time.sleep(1)
        
        self.logger.info("Entering New Password: Password@1 (Same as Current)")
        cp_page.enter_new_password("Password@1")
        time.sleep(1)
        
        self.logger.info("Entering Confirm Password: Password@1")
        cp_page.enter_confirm_password("Password@1")
        time.sleep(2)
        
        self.logger.info("Toggling visibility to show the same passwords...")
        cp_page.toggle_current_visibility()
        cp_page.toggle_new_visibility()
        time.sleep(3)
        
        self.logger.info("Submitting to trigger 'Same as Current' warning...")
        cp_page.click_change_password()
        time.sleep(5) # Observe the warning
        
        # 4. Phase 2: Correcting to Positive Attempt (Password@12)
        self.logger.info("--- Phase 2: Correcting to New Password (Password@12) ---")
        
        self.logger.info("Updating New Password to: Password@12")
        cp_page.enter_new_password("Password@12")
        time.sleep(2)
        self.logger.info("Clicking Eye icon to view corrected new password...")
        cp_page.toggle_new_visibility()
        time.sleep(3)
        
        self.logger.info("Updating Confirm Password to: Password@12")
        cp_page.enter_confirm_password("Password@12")
        time.sleep(2)
        self.logger.info("Clicking Eye icon to view corrected confirm password...")
        cp_page.toggle_confirm_visibility()
        time.sleep(3)
        
        self.logger.info("Waiting 5 seconds before final submission...")
        time.sleep(5)
        
        self.logger.info("Final Submission with Password@12...")
        cp_page.click_change_password()
        
        self.logger.info("Waiting 5 seconds to observe final result...")
        time.sleep(5)
        
        self.logger.info("**** Test_008_ChangePassword Completed Successfully ****")
        time.sleep(2)
