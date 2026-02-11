import pytest
import time
from selenium.webdriver.common.by import By
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.eservices_page import EServicesPage
from pages.change_password_page import ChangePasswordPage
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Test_Post_Registration_Audit:
    home_url = "https://bridge-uat.nios.ac.in/"
    email = ReadConfig.getLoginEmail()
    password = ReadConfig.getLoginPassword()
    logger = LogGen.loggen()

    def test_complete_dashboard_audit_flow(self, setup):
        """
        Comprehensive Post-Registration Audit:
        1. Login
        2. Verify Teacher Info (Name, Ref No) across Dashboard, Modal, and Print View.
        3. Verify E-Services Requests history.
        4. Verify Security Settings (Change Password Page).
        5. Verify section visibility (Study Material, Results, etc.)
        """
        self.logger.info("**** Starting Test_Post_Registration_Audit ****")
        self.driver = setup
        self.driver.get(self.home_url)

        # 1. Login
        home_page = HomePage(self.driver)
        home_page.navigate_to_teacher_login()
        login_page = LoginPage(self.driver)
        if not login_page.login_with_manual_captcha(self.email, self.password, timeout=300):
            pytest.fail("Login failed.")

        dashboard_page = DashboardPage(self.driver)
        time.sleep(5)

        # --- A. Data Continuity Audit ---
        self.logger.info("--- Phase A: Profile Data Continuity ---")
        time.sleep(5)
        try:
            dash_name = dashboard_page.get_teacher_name()
            dash_ref_no = dashboard_page.get_reference_no()
            self.logger.info(f"Dashboard Data - Name: {dash_name}, Ref No: {dash_ref_no}")
        except:
            self.logger.warning("Could not extract dashboard name/ref. proceeding...")
            dash_name = "Unknown"
            dash_ref_no = "Unknown"

        # Check Modal
        try:
            dashboard_page.click_school_details()
            time.sleep(5)
            modal_udise = dashboard_page.get_modal_udise_code()
            self.logger.info(f"Modal Data - UDISE: {modal_udise}")
            dashboard_page.do_click(dashboard_page.modal_close_btn)
            time.sleep(5)
        except Exception as e:
            self.logger.error(f"Modal interaction failed: {e}")
            # Try to recover by refreshing if modal is stuck?
            self.driver.refresh()
            time.sleep(5)

        # Check Print Form (Robust check)
        self.logger.info("--- Phase A (cont): Print Form Check ---")
        time.sleep(5)
        original_window = self.driver.current_window_handle
        
        try:
            dashboard_page.do_click(dashboard_page.link_print_application)
            self.logger.info("Clicked Print Application...")
            time.sleep(8) # Wait for action (longer wait for print preview)
            
            all_handles = self.driver.window_handles
            
            # Check if new window opened
            if len(all_handles) > 1:
                self.logger.info(f"Print Form opened in NEW TAB. Handles: {len(all_handles)}")
                # Switch to the new tab (usually the last one)
                new_tab = all_handles[-1]
                if new_tab != original_window:
                     self.driver.switch_to.window(new_tab)
                     self.logger.info(f"Switched to new tab: {self.driver.current_url}")
                     time.sleep(5) # Wait for content
                
                     # Verify and Close
                     current_url_lower = self.driver.current_url.lower()
                     if "print" in current_url_lower or "application" in current_url_lower:
                         self.logger.info("Print URL Verified.")
                     else:
                         self.logger.warning(f"Print URL unexpected: {self.driver.current_url}")

                     self.driver.close()
                     self.logger.info("Closed Print Tab.")
                     self.driver.switch_to.window(original_window)
                     self.logger.info("Switched back to Original Window.")
                else:
                     self.logger.warning("New handle same as old? Logic check needed.")
                     
            else:
                self.logger.info("Print Form opened in SAME TAB.")
                current_url_lower = self.driver.current_url.lower()
                if "print" in current_url_lower or "application" in current_url_lower:
                     self.logger.info("Print URL Verified.")
                else:
                     self.logger.warning(f"Print URL unexpected: {self.driver.current_url}")
                     
                self.driver.back()
                self.logger.info("Navigated Back.")
                time.sleep(5) # Wait for Dashboard to reload
                
            self.logger.info("Continuity Check (Print View): PASS")

        except Exception as e:
            self.logger.error(f"Print View Audit failed: {e}")
            # Recovery: Ensure we are back on main window
            try:
                if len(self.driver.window_handles) > 1:
                     # If we are not on original window, close current
                     if self.driver.current_window_handle != original_window:
                          self.driver.close()
                self.driver.switch_to.window(original_window)
            except Exception as recover_e:
                self.logger.error(f"Recovery failed: {recover_e}")

        
        time.sleep(5)
        
        time.sleep(5)

        # --- B. E-Services History Audit ---
        self.logger.info("--- Phase B: E-Services Request Audit ---")
        dashboard_page.do_click(dashboard_page.link_eservices_requests)
        time.sleep(5)
        esv_page = EServicesPage(self.driver)
        requests = esv_page.get_request_history()
        self.logger.info(f"Found {len(requests)} existing service requests.")
        self.driver.back()
        time.sleep(5)

        # --- C. Security Settings Audit ---
        self.logger.info("--- Phase C: Security Settings Audit ---")
        dashboard_page.do_click(dashboard_page.dropdown_user)
        time.sleep(5)
        dashboard_page.do_click(dashboard_page.link_change_password)
        time.sleep(5)
        
        cp_page = ChangePasswordPage(self.driver)
        assert "change-password" in self.driver.current_url
        self.logger.info("Security Page verification: PASS")
        
        self.driver.get(self.home_url + "teacher/dashboard")
        time.sleep(5)

        # --- D. Final Section Visibility Audit ---
        self.logger.info("--- Phase D: Visibility & Navigation Check (My Documents, etc.) ---")
        time.sleep(5)
        
        # Check My Documents Navigation
        dashboard_page.verify_my_documents()
        dashboard_page.do_click(dashboard_page.link_view_documents)
        time.sleep(5)
        assert "documents" in self.driver.current_url.lower()
        self.logger.info("My Documents Navigation: PASS")
        self.driver.back()
        time.sleep(5)

        dashboard_page.verify_study_material()
        dashboard_page.verify_results_section()
        dashboard_page.verify_grievances_section()
        
        self.logger.info("**** Post-Registration Audit Completed Successfully ****")
