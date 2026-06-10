from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class OTPPage(BasePage):
    # General Locators for the groups of inputs
    MOBILE_OTP_INPUTS = (By.CSS_SELECTOR, "input.mob-otp-input")
    EMAIL_OTP_INPUTS = (By.CSS_SELECTOR, "input.email-otp-input")

    def enter_mobile_otp(self, otp):
        """Enter a 6-digit mobile OTP."""
        if len(otp) != 6:
            self.logger.error(f"Invalid Mobile OTP length: {len(otp)}. Expected 6.")
            return
            
        # Wait for presence of at least one input
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.MOBILE_OTP_INPUTS))
        inputs = self.driver.find_elements(*self.MOBILE_OTP_INPUTS)
        
        if len(inputs) < 6:
             self.logger.error(f"Found only {len(inputs)} Mobile OTP inputs, expected 6")
             return

        for i, char in enumerate(otp):
            inputs[i].send_keys(char)
        self.logger.info("Entered 6-digit Mobile OTP")

    def enter_email_otp(self, otp):
        """Enter a 6-digit email OTP."""
        if len(otp) != 6:
            self.logger.error(f"Invalid Email OTP length: {len(otp)}. Expected 6.")
            return

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.EMAIL_OTP_INPUTS))
        inputs = self.driver.find_elements(*self.EMAIL_OTP_INPUTS)
        
        if len(inputs) < 6:
             self.logger.error(f"Found only {len(inputs)} Email OTP inputs, expected 6")
             return

        for i, char in enumerate(otp):
            inputs[i].send_keys(char)
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
