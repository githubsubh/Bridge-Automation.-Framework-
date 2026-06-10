import pytest
import time
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.change_password_page import ChangePasswordPage
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen

class Test_Security_Smoke:
    home_url = "https://bridge-uat.nios.ac.in/"
    email = ReadConfig.getLoginEmail()
    password = ReadConfig.getLoginPassword()
    logger = LogGen.loggen()

    def test_verify_change_password_page(self, setup):
        """
        Security Smoke Test:
        1. Login
        2. Navigate to Change Password.
        3. Verify elements and toggle visibility icons.
        4. Do NOT actually change the password (smoke only).
        """
        self.logger.info("**** Starting Test_Security_Smoke ****")
        self.driver = setup
        self.driver.get(self.home_url)

        # 1. Login
        home_page = HomePage(self.driver)
        home_page.navigate_to_teacher_login()
        login_page = LoginPage(self.driver)
        if not login_page.login_with_manual_captcha(self.email, self.password, timeout=120):
            pytest.fail("Login failed.")

        dashboard_page = DashboardPage(self.driver)
        time.sleep(5)

        # 2. Navigate to Change Password
        self.logger.info("Navigating to Change Password via User Dropdown...")
        dashboard_page.do_click(dashboard_page.dropdown_user)
        time.sleep(1)
        dashboard_page.do_click(dashboard_page.link_change_password)
        time.sleep(3)

        cp_page = ChangePasswordPage(self.driver)
        if "change-password" in self.driver.current_url:
            self.logger.info("Successfully reached Change Password page.")
        else:
            pytest.fail("Failed to navigate to Change Password page.")

        # 3. Verify Elements and Toggles
        cp_page.enter_current_password("dummy123")
        cp_page.toggle_current_visibility()
        time.sleep(1)
        
        cp_page.enter_new_password("NewPass123")
        cp_page.toggle_new_visibility()
        time.sleep(1)
        
        cp_page.enter_confirm_password("NewPass123")
        cp_page.toggle_confirm_visibility()
        time.sleep(1)

        self.logger.info("Security Smoke PASS: Page loaded and input fields/toggles are functional.")

        # 4. Return to Dashboard
        self.driver.get(self.home_url + "teacher/dashboard")
        time.sleep(2)
        
        self.logger.info("**** Test_Security_Smoke Completed successfully ****")
