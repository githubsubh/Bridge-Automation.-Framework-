from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class LoginPage(BasePage):
    # Locators
    textbox_email_id = (By.ID, "loginform-email")
    textbox_password_id = (By.ID, "loginform-password")
    textbox_captcha_id = (By.ID, "loginform-verifycode")
    button_login_id = (By.ID, "submit-basic-details")
    
    # Dashboard Verification Locator (adjust based on actual dashboard content)
    # The user mentioned "Syllabus", "eServices" etc. usually appear in a sidebar or header
    # We will look for any reliable element related to the logged-in state.
    # A logout button is a classic indicator.
    link_logout_xpath = (By.XPATH, "//a[contains(text(), 'Logout')]")

    def __init__(self, driver):
        super().__init__(driver)

    def set_email(self, email):
        self.do_send_keys(self.textbox_email_id, email)

    def set_password(self, password):
        self.do_send_keys(self.textbox_password_id, password)

    def click_login(self):
        self.do_click(self.button_login_id)

    def login_with_manual_captcha(self, email, password, timeout=60):
        """
        Enters credentials and then waits for the user to manually enter CAPTCHA and submit.
        """
        self.logger.info("Starting Login Process...")
        
        # Stabilization after navigation
        time.sleep(2)
        
        # Email
        self.logger.info(f"Entering email: {email}")
        self.do_send_keys(self.textbox_email_id, email)
        
        # Password
        self.logger.info("Entering password...")
        self.do_send_keys(self.textbox_password_id, password)
        
        # Visual pause for user check
        time.sleep(1)
        
        # Focus on CAPTCHA field to help user
        try:
            self.do_click(self.textbox_captcha_id)
            self.logger.info("Focused CAPTCHA field")
        except:
            pass

        print("\n" + "="*60)
        print("ATTENTION: CAPTCHA REQUIRED")
        print("1. The script has entered Email and Password.")
        print("2. Please Look at the Browser Window.")
        print("3. Read the CAPTCHA image and Enter it into the text box.")
        print("4. Click the 'Login' button manually.")
        print(f"Waiting up to {timeout} seconds for you to login...")
        print("="*60 + "\n")

        # Wait for login success
        # We can detect success by checking if we are REDIRECTED away from /auth/login 
        # OR if the "Logout" button appears.
        end_time = time.time() + timeout
        while time.time() < end_time:
            current_url = self.driver.current_url
            if "/auth/login" not in current_url and "dashboard" in current_url:
                self.logger.info("Login Detected via URL change!")
                return True
            
            # optional: check for dashboard element
            try:
                if self.driver.find_elements(*self.link_logout_xpath):
                    self.logger.info("Login Detected via Logout button!")
                    return True
            except:
                pass
                
            time.sleep(1)
            
        self.logger.error("Login timed out. User did not complete login in time.")
        return False
        
    def verify_dashboard_elements(self):
        """
        Verifies that 'Syllabus', 'eServices', 'Payments' etc are visible.
        This confirms the user is on the correct dashboard.
        """
        keywords = ["Syllabus", "Points", "Payment"]
        missing = []
        page_source = self.driver.page_source
        
        for keyword in keywords:
            if keyword not in page_source:
                missing.append(keyword)
        
        if missing:
            self.logger.warning(f"Some dashboard elements missing or text different: {missing}")
            return False
        
        self.logger.info("All dashboard keywords found.")
        return True
