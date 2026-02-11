import pytest
import time
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen

class Test_012_DashboardAudit:
    home_url = "https://bridge-uat.nios.ac.in/"
    email = ReadConfig.getLoginEmail()
    password = ReadConfig.getLoginPassword()
    logger = LogGen.loggen()

    def test_dashboard_audit_flow(self, setup):
        self.logger.info("**** Starting Test_012_DashboardAudit ****")
        self.driver = setup
        self.driver.get(self.home_url)

        # 1. Login
        home_page = HomePage(self.driver)
        home_page.navigate_to_teacher_login()

        login_page = LoginPage(self.driver)
        if not login_page.login_with_manual_captcha(self.email, self.password, timeout=120):
            pytest.fail("Login failed, cannot audit Dashboard.")

        self.logger.info("Login successful. Waiting 5 seconds on Dashboard...")
        time.sleep(5)

        dashboard_page = DashboardPage(self.driver)

        # 2. Audit Sidebar Progress
        self.logger.info("--- Phase 1: Sidebar Progress Audit ---")
        if dashboard_page.audit_sidebar_progress():
            self.logger.info("Sidebar Progress Audit: PASSED (100% complete with 5 checkmarks)")
        else:
            self.logger.warning("Sidebar Progress Audit: FAILED or Incomplete checkmarks.")

        # 3. Audit School Details Modal
        self.logger.info("--- Phase 2: School & RC Modal Audit ---")
        dashboard_page.mouse_hover(dashboard_page.btn_school_details)
        time.sleep(5)
        dashboard_page.click_school_details()
        
        # Give modal a second to appear
        time.sleep(5)
        
        if dashboard_page.verify_modal_content():
            self.logger.info("Modal Table Verification: PASSED")
        else:
            pytest.fail("Modal content verification failed.")

        # 4. Visual Inspection Pause
        self.logger.info("Audit phases complete. Waiting 5 seconds for final visual check before logout.")
        time.sleep(5)

        # 5. Logout
        dashboard_page.do_logout()
        self.logger.info("**** Test_012_DashboardAudit Completed Successfully ****")
