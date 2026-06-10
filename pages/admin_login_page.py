from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import os
import time

class AdminLoginPage(BasePage):
    # Locators
    USERNAME_FIELD = (By.ID, "loginform-username")
    PASSWORD_FIELD = (By.ID, "loginform-password")
    CAPTCHA_FIELD = (By.ID, "loginform-verifycode")
    LOGIN_BUTTON = (By.NAME, "login-button")

    def __init__(self, driver):
        super().__init__(driver)

    def login_with_manual_captcha(self, username, password, timeout=60):
        """Enters credentials and waits for manual CAPTCHA and login."""
        self.logger.info(f"Starting Admin Login for {username}...")
        self.do_send_keys(self.USERNAME_FIELD, username)
        self.do_send_keys(self.PASSWORD_FIELD, password)
        
        print("\n" + "="*60)
        print("ADMIN CAPTCHA REQUIRED")
        print("Please solve the CAPTCHA and click LOGIN in the browser.")
        print(f"Waiting up to {timeout} seconds...")
        print("="*60 + "\n")

        import time
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                # If we see a Logout link or button, we are in.
                if self.driver.find_elements(By.XPATH, "//*[translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='logout' or contains(text(), 'Logout') or contains(text(), 'Sign Out')]"):
                    self.logger.info("Admin login detected! Logout button found.")
                    return True
            except:
                pass
            time.sleep(1)
        
        self.logger.error("Admin login timed out.")
        return False

    def login(self, username, password):
        """Login to the admin portal.
        If the environment variable SKIP_CAPTCHA is true, credentials are entered and login is attempted without waiting for manual CAPTCHA.
        """
        if os.getenv("SKIP_CAPTCHA", "false").lower() == "true":
            # Fast path: fill credentials, click login, short pause
            self.do_send_keys(self.USERNAME_FIELD, username)
            self.do_send_keys(self.PASSWORD_FIELD, password)
            self.do_click(self.LOGIN_BUTTON)
            time.sleep(2)
            return True
        # Default behavior – manual captcha handling
        return self.login_with_manual_captcha(username, password)
