from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time

class HomePage(BasePage):
    # Locators
    # Using generic text locators based on visual description
    link_login_corner_xpath = (By.XPATH, "//a[contains(., 'Login Corner') or contains(text(), 'Login Corner')]")
    link_teacher_login_xpath = (By.XPATH, "//a[contains(., 'Teacher Login') or contains(text(), 'Teacher Login')]")

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_teacher_login(self):
        """Waits on home page, then navigates to Teacher Login."""
        self.logger.info("Accessing Home Page...")
        
        # User requested 5 second wait on Home Page
        self.logger.info("Home Page Loaded. Waiting 5 seconds...")
        time.sleep(5)
        
        self.logger.info("Attempting to hover 'Login Corner' and click 'Teacher Login'...")
        from selenium.webdriver import ActionChains
        actions = ActionChains(self.driver)
        
        # Store original handle
        original_window = self.driver.current_window_handle
        
        try:
            login_corner = self.driver.find_element(*self.link_login_corner_xpath)
            actions.move_to_element(login_corner).perform()
            time.sleep(1)
            
            teacher_login = self.driver.find_element(*self.link_teacher_login_xpath)
            teacher_login.click()
            time.sleep(2) # Give it time to open
            
            # Check for new windows
            handles = self.driver.window_handles
            if len(handles) > 1:
                self.logger.info("New window detected, switching to it and closing original...")
                for h in handles:
                    if h != original_window:
                        self.driver.switch_to.window(h)
                        break
                # Close the home page window if we are redirected to login in a new one
                # But only if the new url is actually login
                if "login" in self.driver.current_url.lower():
                    # Switch back to original to close it, then back to new
                    # Actually easier to just stay on new and let script continue
                    pass

        except Exception as e:
            self.logger.warning(f"Standard navigation failed: {e}. Trying direct click.")
            self.do_click(self.link_teacher_login_xpath)

        # Final check/Fallback
        if "login" not in self.driver.current_url.lower():
            self.logger.info("Still not on login page. Using direct navigation...")
            self.driver.get("https://bridge-uat.nios.ac.in/auth/login")
        
        self.logger.info(f"Final URL: {self.driver.current_url}")
        self.logger.info("Navigated to Teacher Login Page.")
