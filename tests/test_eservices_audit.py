import pytest
import time
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.eservices_page import EServicesPage
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen

class Test_013_EServicesAudit:
    home_url = "https://bridge-uat.nios.ac.in/"
    email = ReadConfig.getLoginEmail()
    password = ReadConfig.getLoginPassword()
    logger = LogGen.loggen()

    def test_eservices_audit_flow(self, setup):
        self.logger.info("**** Starting Test_013_EServicesAudit ****")
        self.driver = setup
        self.driver.get(self.home_url)

        # 1. Login
        home_page = HomePage(self.driver)
        home_page.navigate_to_teacher_login()

        login_page = LoginPage(self.driver)
        if not login_page.login_with_manual_captcha(self.email, self.password, timeout=120):
            pytest.fail("Login failed, cannot audit E-Services.")

        self.logger.info("Login successful. Navigating to E-Services...")
        time.sleep(3)

        dashboard_page = DashboardPage(self.driver)
        eservices_page = EServicesPage(self.driver)

        # 2. Audit: Apply E-Services
        self.logger.info("--- Phase 1: Available E-Services Audit ---")
        # Direct navigation to avoid click interceptions
        self.driver.get(self.home_url + "eservices/apply")
        time.sleep(5)
        
        # Verify page title or header from DOM
        if "Apply for E-Services" in self.driver.title:
            self.logger.info("E-Services Apply page title verified.")
        else:
            self.logger.warning(f"Unexpected title: {self.driver.title}")

        service_count = eservices_page.get_service_count()
        if service_count > 0:
            self.logger.info(f"Audit PASSED: Found {service_count} available services.")
        else:
            self.logger.warning("Audit WARNING: No service links found.")

        # 3. Audit: My Requests
        self.logger.info("--- Phase 2: My Request History Audit ---")
        self.driver.get(self.home_url + "eservices/requests")
        time.sleep(5)
        
        if eservices_page.is_visible(eservices_page.header_my_requests):
            self.logger.info("My Requests page header verified via DOM header.")
            history = eservices_page.get_request_history()
            self.logger.info(f"Audit PASSED: Found {len(history)} existing request(s).")
            for req in history:
                self.logger.info(f"Verified Request: {req['request_id']} | {req['type']} | {req['status']}")
        else:
            # Fallback check for title
            if "Your E-Service Requests" in self.driver.title:
                self.logger.info("My Requests page verified via Title.")
            else:
                pytest.fail("Failed to verify My Requests page.")

        # 4. Final inspection
        self.logger.info("E-Services Audit complete. Waiting 5s before logout...")
        time.sleep(5)
        
        # 5. Logout
        dashboard_page.do_logout()
        self.logger.info("**** Test_013_EServicesAudit Completed Successfully ****")
