from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class OTPPage(BasePage):
    # Locators for individual digits
    # Mobile OTP
    def get_mob_otp_locator(self, digit_index):
        # digit_index 1 to 6
        return (By.CSS_SELECTOR, f"input.mob-otp-input[aria-label='Mobile OTP digit {digit_index}']")

    # Email OTP
    def get_email_otp_locator(self, digit_index):
        # digit_index 1 to 6
        return (By.CSS_SELECTOR, f"input.email-otp-input[aria-label='Email OTP digit {digit_index}']")

    button_verify_xpath = (By.XPATH, "//button[@type='submit' or contains(text(), 'Verify') or contains(text(), 'CONTINUE')]")

    def __init__(self, driver):
        super().__init__(driver)

    def enter_mobile_otp(self, otp):
        """Enter a 6-digit mobile OTP."""
        if len(otp) != 6:
            self.logger.error(f"Invalid Mobile OTP length: {len(otp)}. Expected 6.")
            return
        for i in range(1, 7):
            locator = self.get_mob_otp_locator(i)
            self.do_send_keys(locator, otp[i-1])
        self.logger.info("Entered 6-digit Mobile OTP")

    def enter_email_otp(self, otp):
        """Enter a 6-digit email OTP."""
        if len(otp) != 6:
            self.logger.error(f"Invalid Email OTP length: {len(otp)}. Expected 6.")
            return
        for i in range(1, 7):
            locator = self.get_email_otp_locator(i)
            self.do_send_keys(locator, otp[i-1])
        self.logger.info("Entered 6-digit Email OTP")

    def click_verify(self):
        try:
            self.do_click(self.button_verify_xpath)
            self.logger.info("Clicked Verify button on OTP page")
        except Exception as e:
            self.logger.warning(f"Standard click failed, trying JS: {e}")
            element = self.driver.find_element(*self.button_verify_xpath)
            self.driver.execute_script("arguments[0].click();", element)
            self.logger.info("Clicked Verify on OTP page using JS")
