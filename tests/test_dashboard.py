import pytest
import time
import os
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen

class Test_003_DashboardFeatures:
    # Read config
    login_url = ReadConfig.getLoginURL()
    email = ReadConfig.getLoginEmail()
    password = ReadConfig.getLoginPassword()
    logger = LogGen.loggen()
    timeouts = ReadConfig.getTimeouts()
    
    def test_dashboard_features(self, setup):
        self.logger.info("**** Starting Test_003_DashboardFeatures (OPTIMIZED) ****")
        self.driver = setup
        self.driver.get(self.login_url)
        
        try:
            # 1. Login Phase
            login_page = LoginPage(self.driver)
            self.logger.info("Logging in to access Dashboard...")
            
            # Use config timeout instead of hardcoded value
            login_timeout = self.timeouts.get('captcha_wait', 120)
            if not login_page.login_with_manual_captcha(self.email, self.password, timeout=login_timeout):
                self._capture_failure("login_failed")
                pytest.fail("Login failed, cannot test dashboard.")
            
            self.logger.info("✅ Login successful - Dashboard loaded")
            
            # Ensure Chrome window is visible and in front
            try:
                self.driver.set_window_position(0, 0)
                self.driver.maximize_window()
                self.driver.execute_script("window.focus();")
                self.logger.info("Chrome window brought to front")
            except Exception as e:
                self.logger.warning(f"Could not position window: {e}")
            
            time.sleep(3)  # Wait for dashboard to stabilize (increased for visibility)
                
            # 2. Dashboard Verification Phase
            dashboard_page = DashboardPage(self.driver)
            verification_results = {}
            
            # Verify Features One by One with strategic waits
            sections = [
                ("Study Material", dashboard_page.verify_study_material),
                ("E-Services", dashboard_page.verify_eservices),
                ("Payment Status", dashboard_page.verify_payment_status),
                ("My Documents", dashboard_page.verify_my_documents),
                ("Print Section", dashboard_page.verify_print_section),
                ("Results", dashboard_page.verify_results_section),
                ("Grievances", dashboard_page.verify_grievances_section),
                ("Workflow", dashboard_page.verify_workflow)
            ]
            
            for idx, (section_name, verify_func) in enumerate(sections, 1):
                self.logger.info(f"--- {idx}. {section_name} Check ---")
                
                try:
                    result = verify_func()
                    verification_results[section_name] = result
                    
                    if result:
                        self.logger.info(f"✅ {section_name} section verified successfully")
                    else:
                        self.logger.error(f"❌ {section_name} section verification failed")
                        self._capture_failure(f"{section_name.lower().replace(' ', '_')}_verification_failed")
                    
                    assert result, f"{section_name} Section Verification Failed"
                    
                    # LONGER strategic wait between verifications for visibility
                    if idx < len(sections):
                        time.sleep(2)  # 2 seconds so user can see each verification
                        
                except Exception as e:
                    self.logger.error(f"Exception during {section_name} verification: {e}")
                    self._capture_failure(f"{section_name.lower().replace(' ', '_')}_exception")
                    raise
            
            # Log summary of verifications
            self.logger.info("=== Verification Summary ===")
            passed = sum(1 for v in verification_results.values() if v)
            total = len(verification_results)
            self.logger.info(f"Passed: {passed}/{total}")
            for section, result in verification_results.items():
                status = "✅ PASS" if result else "❌ FAIL"
                self.logger.info(f"{status} - {section}")
            
            time.sleep(3)  # Pause so user can see summary before logout
            
            # Capture DOM before logout for debugging
            self.logger.info("Capturing dashboard DOM before logout...")
            self._save_dom("dashboard_pre_logout.html")
            
            # 9. Logout Check
            self.logger.info("--- 9. Logout Check ---")
            initial_url = self.driver.current_url
            self.logger.info(f"Current URL before logout: {initial_url}")
            
            logout_success = dashboard_page.do_logout()
            
            if logout_success:
                # Verify logout redirection
                time.sleep(2)
                final_url = self.driver.current_url
                self.logger.info(f"Current URL after logout: {final_url}")
                
                # Check if redirected to login or home
                if "login" in final_url.lower() or "auth" in final_url.lower() or final_url.endswith("/"):
                    self.logger.info("✅ Logout successful - Redirected to login/home page")
                else:
                    self.logger.warning(f"⚠️ Logout URL unexpected: {final_url}")
                    self._capture_failure("logout_redirect_unexpected")
            else:
                self.logger.error("❌ Logout function returned False")
                self._capture_failure("logout_failed")
                pytest.fail("Logout failed")
            
            self.logger.info("**** Test_003_DashboardFeatures Passed Successfully ****")
            
        except Exception as e:
            self.logger.error(f"Test failed with exception: {e}")
            self._capture_failure("test_exception")
            raise
    
    def _save_dom(self, filename):
        """Save current page DOM to file for debugging"""
        try:
            dom_path = os.path.join(os.getcwd(), filename)
            with open(dom_path, "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            self.logger.info(f"DOM saved to: {filename}")
        except Exception as e:
            self.logger.warning(f"Could not save DOM: {e}")
    
    def _capture_failure(self, failure_name):
        """Capture screenshot and DOM on failure"""
        try:
            # Create screenshots directory if it doesn't exist
            screenshots_dir = os.path.join(os.getcwd(), "screenshots")
            if not os.path.exists(screenshots_dir):
                os.makedirs(screenshots_dir)
            
            # Save screenshot
            screenshot_path = os.path.join(screenshots_dir, f"dashboard_{failure_name}.png")
            self.driver.save_screenshot(screenshot_path)
            self.logger.info(f"Screenshot saved: {screenshot_path}")
            
            # Save DOM
            dom_filename = f"dashboard_{failure_name}.html"
            self._save_dom(dom_filename)
            
        except Exception as e:
            self.logger.warning(f"Could not capture failure artifacts: {e}")
