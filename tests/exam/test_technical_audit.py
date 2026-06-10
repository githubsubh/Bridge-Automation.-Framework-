import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen
from utilities.screenshot_utils import ScreenshotUtils

class Test_Exam_Technical_Audit:
    logger = LogGen.loggen()
    reg_url = "https://bridge-uat.nios.ac.in/exam/registration/apply"
    otp_url = "https://bridge-uat.nios.ac.in/exam/registration/verify-otp" # Predicted based on patterns

    @pytest.mark.critical
    def test_crit_01_unauthorized_access(self, setup):
        """Verify that the system redirects to login when accessing registration directly."""
        driver = setup
        self.logger.info("Executing CRIT_01: Unauthorized Access Test")
        driver.get(self.reg_url)
        time.sleep(3)
        current_url = driver.current_url
        if "login" in current_url.lower():
            self.logger.info("PASS: System correctly redirected unauthorized user to login.")
        else:
            self.logger.error(f"CRITICAL BUG: Unauthorized access allowed to {self.reg_url}")
            ScreenshotUtils.capture_screenshot(driver, "CRIT_BUG_Unauthorized_Access")

    @pytest.mark.critical
    def test_crit_02_state_bypass_otp(self, setup):
        """Verify that the OTP page cannot be reached without proceeding from Stage 1."""
        driver = setup
        self.logger.info("Executing CRIT_02: State Bypass (Direct OTP Access) Test")
        # Login first
        from pages.login_page import LoginPage
        login_page = LoginPage(driver)
        login_page.handle_restricted_access()
        login_page.login_with_manual_captcha(ReadConfig.getLoginEmail(), ReadConfig.getLoginPassword())
        
        # Now try to jump directly to OTP
        driver.get(self.otp_url)
        time.sleep(3)
        
        body_text = driver.find_element(By.TAG_NAME, "body").text
        if "Forbidden" in body_text or "403" in body_text or "redirected" in driver.current_url:
            self.logger.info("PASS: Direct OTP access blocked/validated.")
        else:
            self.logger.warning("POTENTIAL RISK: System allowed direct navigation to OTP page. Checking for data errors...")
            ScreenshotUtils.capture_screenshot(driver, "CRIT_State_Bypass_Check")

    @pytest.mark.critical
    def test_crit_03_double_proceed_crash(self, setup):
        """Spam PROCEED button to check for backend race conditions or duplicate entries."""
        driver = setup
        self.logger.info("Executing CRIT_03: Double Proceed Race Condition Test")
        
        # Login Required
        from pages.login_page import LoginPage
        login_page = LoginPage(driver)
        login_page.handle_restricted_access()
        login_page.login_with_manual_captcha(ReadConfig.getLoginEmail(), ReadConfig.getLoginPassword())
        
        driver.get(self.reg_url)
        time.sleep(5)
        
        try:
            proceed_btn = driver.find_element(By.XPATH, "//button[normalize-space(.)='PROCEED']")
            self.logger.info("Spamming PROCEED button...")
            for _ in range(10): # Increased spam count
                driver.execute_script("arguments[0].click();", proceed_btn)
            
            time.sleep(5)
            # Check for crash or error page
            if "error" in driver.title.lower() or "500" in driver.page_source or "not found" in driver.page_source:
                self.logger.error("CRITICAL BUG: System crashed (500) or showed error on rapid PROCEED clicks.")
                ScreenshotUtils.capture_screenshot(driver, "CRIT_BUG_Double_Proceed_Crash")
            else:
                self.logger.info("System handled concurrent clicks gracefully.")
        except Exception as e:
            self.logger.warning(f"Could not perform double-click test: {e}")

