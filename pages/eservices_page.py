from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time

class EServicesPage(BasePage):
    # --- Locators ---
    
    # Apply Section
    header_apply = (By.XPATH, "//h1[contains(text(), 'Available E-Services')]")
    # All edit icons/links
    links_apply_icons = (By.XPATH, "//a[contains(@href, '/eservices/verify-otp')]")
    
    # My Requests Section
    header_requests = (By.XPATH, "//h5[contains(text(), 'My E-Service Requests')]")
    table_requests = (By.TAG_NAME, "table")

    def __init__(self, driver):
        super().__init__(driver)

    def verify_apply_page(self):
        """Verifies visibility of the Apply for E-Services page."""
        self.logger.info("Checking Apply E-Services page...")
        return self.is_visible(self.header_apply)

    def verify_requests_page(self):
        """Verifies visibility of the My Requests page."""
        self.logger.info("Checking My E-Service Requests page...")
        # If header_requests is not found, maybe look for table or similar text
        return self.is_visible(self.header_requests) or self.is_visible(self.table_requests)

    def click_service_by_name(self, service_name):
        """
        Clicks the apply icon for a specific service name.
        Example names: 'Change Appointment Date', 'Change Correspondence Address', etc.
        """
        self.logger.info(f"Attempting to click service: {service_name}")
        # Find the <strong> tag with text and then get its parent/neighbor <a> tag
        xpath = f"//li[.//strong[contains(text(), '{service_name}')]]//a[contains(@href, '/eservices/verify-otp')]"
        try:
            element = self.driver.find_element(By.XPATH, xpath)
            self.do_click((By.XPATH, xpath))
            self.logger.info(f"Successfully clicked service: {service_name}")
            return True
        except Exception as e:
            self.logger.error(f"Could not find or click service '{service_name}': {e}")
            return False
