from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utilities.wait_utils import WaitUtils
from utilities.otp_utils import OTPUtils
from constants.exam_constants import ExamConstants

class OTPVerificationPage(BasePage):
    # --- Locators ---
    OTP_INPUT = (By.ID, "otp-verification-field")
    CONFIRM_REG_BTN = (By.XPATH, "//button[contains(text(), 'Confirm Registration')]")
    SUCCESS_ALERT = (By.XPATH, "//div[contains(@class, 'alert-success') or contains(text(), 'successful')]")
    ERROR_ALERT = (By.XPATH, "//div[contains(@class, 'alert-danger') or contains(@class, 'error-message')]")
    RESEND_OTP_LINK = (By.LINK_TEXT, "Resend OTP")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait_utils = WaitUtils(self.driver)

    def validate_otp_page(self):
        """Validates that the OTP page has loaded correctly."""
        self.logger.info("Validating OTP Verification page...")
        is_visible = self.is_visible(self.OTP_INPUT)
        self.logger.info(f"OTP input visibility: {is_visible}")
        return is_visible

    def wait_for_manual_otp_entry(self):
        """Pauses execution and waits for manual OTP entry."""
        self.logger.info("Waiting for manual OTP entry by tester...")
        # Use utility to wait for field population
        OTPUtils.wait_for_manual_otp(self.driver, self.OTP_INPUT, timeout=ExamConstants.MANUAL_OTP_TIMEOUT)

    def click_confirm_registration(self):
        """Clicks the Confirm Registration button."""
        self.logger.info("Clicking Confirm Registration...")
        self.wait_utils.clickable_wait(self.CONFIRM_REG_BTN).click()

    def validate_registration_success(self):
        """Validates that the registration success message is displayed."""
        self.logger.info("Validating registration success message...")
        try:
            # Check success alert
            success_element = self.wait_utils.visibility_wait(self.SUCCESS_ALERT)
            success_msg = success_element.text
            self.logger.info(f"Success Message Detected: {success_msg}")
            
            # Additional check: Is the registration button now gone or disabled?
            is_button_gone = self.wait_for_invisibility(self.CONFIRM_REG_BTN)
            
            return (ExamConstants.REGISTRATION_SUCCESS_MSG.lower() in success_msg.lower() or 
                    "successful" in success_msg.lower())
        except Exception as e:
            self.logger.error(f"Success message not found: {e}")
            return False

    def get_error_message(self):
        """Retrieves any visible error message on the OTP page."""
        self.logger.info("Checking for error messages on OTP page...")
        try:
            error_msg = self.wait_utils.visibility_wait(self.ERROR_ALERT).text
            self.logger.warning(f"Error Message Detected: {error_msg}")
            return error_msg
        except:
            self.logger.info("No error message visible.")
            return None

    def click_resend_otp(self):
        """Clicks the Resend OTP link."""
        self.logger.info("Clicking Resend OTP...")
        self.do_click(self.RESEND_OTP_LINK)
