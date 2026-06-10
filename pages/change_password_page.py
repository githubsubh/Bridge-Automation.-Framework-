from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time

class ChangePasswordPage(BasePage):
    # Locators
    txt_current_password = (By.ID, "changepasswordform-currentpassword")
    txt_new_password = (By.ID, "changepasswordform-newpassword")
    txt_confirm_password = (By.ID, "changepasswordform-confirmpassword")
    btn_submit = (By.XPATH, "//button[@type='submit']")
    
    # Eye Icons (Toggle Password)
    eye_current = (By.XPATH, "//div[contains(@class, 'field-changepasswordform-currentpassword')]//span[contains(@class, 'toggle-password')]")
    eye_new = (By.XPATH, "//div[contains(@class, 'field-changepasswordform-newpassword')]//span[contains(@class, 'toggle-password')]")
    eye_confirm = (By.XPATH, "//div[contains(@class, 'field-changepasswordform-confirmpassword')]//span[contains(@class, 'toggle-password')]")

    def toggle_current_visibility(self):
        self.do_click(self.eye_current)
        self.logger.info("Toggled current password visibility.")

    def toggle_new_visibility(self):
        self.do_click(self.eye_new)
        self.logger.info("Toggled new password visibility.")

    def toggle_confirm_visibility(self):
        self.do_click(self.eye_confirm)
        self.logger.info("Toggled confirm password visibility.")

    def enter_current_password(self, password):
        self.do_send_keys(self.txt_current_password, password)
        self.logger.info("Entered current password.")

    def enter_new_password(self, password):
        self.do_send_keys(self.txt_new_password, password)
        self.logger.info("Entered new password.")

    def enter_confirm_password(self, password):
        self.do_send_keys(self.txt_confirm_password, password)
        self.logger.info("Entered confirm password.")

    def click_change_password(self):
        self.do_click(self.btn_submit)
        self.logger.info("Clicked Change Password submit button.")
