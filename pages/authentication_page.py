from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class AuthenticationPage(BasePage):
    # Locators
    textbox_email_id = (By.ID, "authenticationform-email")
    textbox_mobile_id = (By.ID, "authenticationform-mobile_no")
    # Generic submit button locator, covering common labels
    button_submit_xpath = (By.XPATH, "//button[@type='submit' or contains(text(), 'Submit') or contains(text(), 'Send OTP') or contains(text(), 'Next') or contains(text(), 'Continue')]")

    def __init__(self, driver):
        super().__init__(driver)

    def set_email(self, email):
        self.do_send_keys(self.textbox_email_id, email)

    def set_mobile(self, mobile):
        self.do_send_keys(self.textbox_mobile_id, mobile)

    def click_submit(self):
        try:
            self.do_click(self.button_submit_xpath)
            self.logger.info("Clicked Submit/Continue on Authentication page")
        except Exception as e:
            self.logger.warning(f"Standard click failed, trying JS: {e}")
            element = self.driver.find_element(*self.button_submit_xpath)
            self.driver.execute_script("arguments[0].click();", element)
            self.logger.info("Clicked Submit/Continue on Authentication page using JS")
