import pytest
import time
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.eservices_page import EServicesPage
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen
from selenium.webdriver.common.by import By

class Test_Smoke_Dashboard_Links:
    home_url = "https://bridge-uat.nios.ac.in/"
    email = ReadConfig.getLoginEmail()
    password = ReadConfig.getLoginPassword()
    logger = LogGen.loggen()

    def test_verify_all_dashboard_links(self, setup):
        """
        Smoke Test:
        1. Login
        2. Verify all major dashboard links exist and return valid HREFs.
        3. Click internal links and verify landing page context.
        4. No external website automation.
        """
        self.logger.info("**** Starting Test_Smoke_Dashboard_Links ****")
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

        # 2. List of Links to Verify (Internal)
        internal_links = {
            "Payment History": dashboard_page.link_payment_history,
            "View Documents": dashboard_page.link_view_documents,
            "E-Services Apply": dashboard_page.link_eservices_apply,
            "E-Services My Requests": dashboard_page.link_eservices_requests,
            "Study Material Download": dashboard_page.link_download_study_material
        }

        self.logger.info("--- Phase 1: Internal Link Verification ---")
        for name, locator in internal_links.items():
            try:
                elem = self.driver.find_element(*locator)
                href = elem.get_attribute("href")
                self.logger.info(f"Link '{name}' is active. URL: {href}")
                assert href is not None and "nios.ac.in" in href
            except Exception as e:
                self.logger.error(f"Link '{name}' verification failed: {e}")
                pytest.fail(f"Link {name} missing or broken.")

        # 3. Phase 2: Internal Page Content Check (My Requests as a sample)
        self.logger.info("--- Phase 2: Internal Page Context Check ---")
        dashboard_page.do_click(dashboard_page.link_eservices_requests)
        time.sleep(3)
        
        esv_page = EServicesPage(self.driver)
        if "eservices/requests" in self.driver.current_url:
            self.logger.info("Successfully reached 'My Requests' page.")
            history = esv_page.get_request_history()
            self.logger.info(f"Found {len(history)} previous e-service requests.")
        else:
            self.logger.error("Failed to reach E-Services Requests page.")
            pytest.fail("Navigation to E-Services Requests failed.")

        # Go back to Dashboard
        self.driver.get(self.home_url + "teacher/dashboard")
        time.sleep(2)

        # 4. Phase 3: External Link Smoke Check (Just verify existence/clickability)
        self.logger.info("--- Phase 3: External Link Verification (No Automation) ---")
        external_links = {
            "Grievances": dashboard_page.link_submit_grievance
        }
        
        for name, locator in external_links.items():
            try:
                elem = self.driver.find_element(*locator)
                href = elem.get_attribute("href")
                self.logger.info(f"External Link '{name}' found. Points to: {href}")
            except Exception as e:
                self.logger.warning(f"External link '{name}' not found.")

        self.logger.info("**** Smoke Test Completed successfully ****")
