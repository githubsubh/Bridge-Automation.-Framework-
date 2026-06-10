import pytest
import time
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.exam.exam_registration_page import ExamRegistrationPage
from pages.exam.otp_verification_page import OTPVerificationPage
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen
from utilities.screenshot_utils import ScreenshotUtils

class Test_Exam_Registration:
    baseURL = ReadConfig.getApplicationURL()
    loginURL = ReadConfig.getLoginURL()
    email = ReadConfig.getLoginEmail()
    password = ReadConfig.getLoginPassword()
    logger = LogGen.loggen()

    @pytest.mark.exam
    def test_exam_registration_flow(self, setup):
        self.logger.info("**** Starting Test_Exam_Registration_Flow ****")
        self.driver = setup
        self.driver.get(self.loginURL)
        
        # 1. Login Flow
        login_page = LoginPage(self.driver)
        login_page.handle_restricted_access()
        success = login_page.login_with_manual_captcha(self.email, self.password, timeout=120)
        assert success, "Login failed or timed out during CAPTCHA entry."
        time.sleep(3) # Wait for dashboard to settle
        
        # 2. Dashboard Navigation
        dashboard = DashboardPage(self.driver)
        self.logger.info("Verifying Dashboard load...")
        assert "dashboard" in self.driver.current_url.lower(), f"Dashboard did not load successfully. Current URL: {self.driver.current_url}"
        
        # Close 'School Details' modal if it pops up automatically
        try:
            if dashboard.is_visible(dashboard.modal_close_btn):
                self.logger.info("Closing automatic Dashboard modal...")
                dashboard.do_click(dashboard.modal_close_btn)
                time.sleep(1)
        except:
            pass
            
        exam_reg_page = ExamRegistrationPage(self.driver)
        exam_reg_page.navigate_to_exam_registration()
        
        # Pre-check: Is user already registered?
        if exam_reg_page.check_already_registered():
            self.logger.warning("User is already registered. Skipping remaining steps for positive flow.")
            pytest.skip("User already registered. Test case skipped to avoid duplicate data issues.")

        # 3. Active Exam Session Page Validation
        self.logger.info("Validating Active Exam Session page...")
        session_details = exam_reg_page.validate_active_session()
        assert session_details["Academic Year"] != "", "Academic Year is empty"
        assert session_details["Block"] != "", "Block is empty"
        
        # 4. Subject Validation
        subjects = exam_reg_page.get_subjects_list()
        assert len(subjects) > 0, "No subjects found in the table"
        assert exam_reg_page.validate_subjects_data(subjects), "Subject data integrity check failed"
        
        # 5. Proceed Action
        assert exam_reg_page.validate_proceed_button(), "Proceed button is not visible/clickable"
        exam_reg_page.click_proceed()
        
        # 6. OTP Verification Flow
        otp_page = OTPVerificationPage(self.driver)
        assert otp_page.validate_otp_page(), "Failed to load OTP Verification page"
        
        # Manual OTP Entry (Pauses automation)
        try:
            self.logger.info("Awaiting manual OTP entry on browser...")
            otp_page.wait_for_manual_otp_entry()
            otp_page.click_confirm_registration()
            
            # 7. Registration Confirmation
            self.logger.info("Verifying registration success...")
            reg_success = otp_page.validate_registration_success()
            
            if reg_success:
                self.logger.info("**** Exam Registration Successful! ****")
            else:
                error_msg = otp_page.get_error_message()
                self.logger.error(f"Registration failed. Error: {error_msg}")
                ScreenshotUtils.capture_screenshot(self.driver, "Exam_Reg_Failure")
                pytest.fail(f"Exam registration failed. UI Error: {error_msg}")
                
        except Exception as e:
            self.logger.error(f"Error during OTP/Confirmation flow: {e}")
            ScreenshotUtils.capture_screenshot(self.driver, "Exam_Reg_Error")
            pytest.fail(f"Test failed due to exception: {e}")

        self.logger.info("**** Finished Test_Exam_Registration_Flow ****")
