import pytest
import time
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.change_password_page import ChangePasswordPage
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen

class Test_Functional_Security:
    home_url = "https://bridge-uat.nios.ac.in/"
    email = ReadConfig.getLoginEmail()
    old_password = ReadConfig.getLoginPassword()
    new_password = "P@ssword1234!" # Using a strong temporary password
    logger = LogGen.loggen()

    def test_change_password_cycle(self, setup):
        """
        Functional Test: Full Change Password Cycle
        1. Login with Old Password
        2. Change to New Password
        3. Logout
        4. Login with New Password (Verification)
        5. Change back to Old Password (Rollback)
        6. Verify original password works.
        """
        self.logger.info("**** Starting Test_Functional_Security: Change Password Cycle ****")
        self.driver = setup
        self.driver.get(self.home_url)

        # --- 1. LOGIN WITH OLD PASSWORD ---
        lp = LoginPage(self.driver)
        hp = HomePage(self.driver)
        hp.navigate_to_teacher_login()
        if not lp.login_with_manual_captcha(self.email, self.old_password, timeout=120):
            pytest.fail("Initial login failed.")
        self.logger.info("Phase 1: Login with current password successful.")

        dp = DashboardPage(self.driver)
        cp = ChangePasswordPage(self.driver)

        try:
            # --- 2. CHANGE TO NEW PASSWORD ---
            self.logger.info("Phase 2: Changing password to NEW...")
            dp.do_click(dp.dropdown_user)
            time.sleep(1)
            dp.do_click(dp.link_change_password)
            time.sleep(2)

            cp.enter_current_password(self.old_password)
            cp.enter_new_password(self.new_password)
            cp.enter_confirm_password(self.new_password)
            cp.click_change_password()
            time.sleep(5) # Wait for success message/redirect

            # --- 3. LOGOUT ---
            self.logger.info("Phase 3: Logging out...")
            dp.do_logout()
            time.sleep(3)

            # --- 4. LOGIN WITH NEW PASSWORD ---
            self.logger.info("Phase 4: Verifying login with NEW password...")
            hp.navigate_to_teacher_login()
            if not lp.login_with_manual_captcha(self.email, self.new_password, timeout=120):
                pytest.fail("Login with NEW password failed! Security breach or logic error.")
            self.logger.info("Success: Login with NEW password verified.")

            # --- 5. CHANGE BACK TO OLD PASSWORD (ROLLBACK) ---
            self.logger.info("Phase 5: Rolling back to OLD password...")
            dp.do_click(dp.dropdown_user)
            time.sleep(1)
            dp.do_click(dp.link_change_password)
            time.sleep(2)

            cp.enter_current_password(self.new_password)
            cp.enter_new_password(self.old_password)
            cp.enter_confirm_password(self.old_password)
            cp.click_change_password()
            time.sleep(5)

            # --- 6. FINAL VERIFICATION ---
            self.logger.info("Phase 6: Final check of original password...")
            dp.do_logout()
            time.sleep(2)
            hp.navigate_to_teacher_login()
            if not lp.login_with_manual_captcha(self.email, self.old_password, timeout=120):
                pytest.fail("Rollback failed! System left in inconsistent state.")
            
            self.logger.info("**** Functional Security Test: PASSED (Full Cycle) ****")

        except Exception as e:
            self.logger.error(f"Functional Test Exception: {e}")
            # In a real environment, we'd have a recovery script to reset DB if this hangs
            pytest.fail(f"Test failed during functional cycle: {e}")
