from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class DashboardPage(BasePage):
    # --- Locators ---
    
    # Study Material
    header_study_material = (By.XPATH, "//h6[contains(text(), 'Study Material')]")
    link_download_study_material = (By.XPATH, "//a[@href='/study-material/available-subjects']")
    
    # E-Services
    header_eservices = (By.XPATH, "//h6[contains(text(), 'E-Services')]")
    link_eservices_apply = (By.XPATH, "//a[@href='/eservices/apply']")
    link_eservices_requests = (By.XPATH, "//a[@href='/eservices/requests']")
    
    # Payment Status
    header_payment_status = (By.XPATH, "//h6[contains(text(), 'Payment Status')]")
    link_payment_history = (By.XPATH, "//a[@href='/transactions']")
    
    # Workflow / Registration Steps
    header_reg_steps = (By.XPATH, "//h5[contains(text(), 'Registration Steps')]")
    progress_bar = (By.CLASS_NAME, "progress-bar")
    
    # Recent Activities
    header_recent_activities = (By.XPATH, "//h5[contains(text(), 'Recent Activities')]")
    
    # Header & Logout
    dropdown_user = (By.ID, "dropdownMenuLink")
    link_logout = (By.XPATH, "//a[@href='/auth/logout']")

    def __init__(self, driver):
        super().__init__(driver)

    def verify_study_material(self):
        """Verifies the Study Material section exists and has the Download link."""
        self.logger.info("Verifying Study Material Section...")
        if self.is_visible(self.header_study_material):
            self.logger.info("Study Material Header found.")
            if self.is_visible(self.link_download_study_material):
                self.logger.info("Study Material 'Download' link found.")
                return True
        self.logger.error("Study Material section missing or incomplete.")
        return False

    def verify_eservices(self):
        """Verifies the E-Services section exists and has Apply/My Requests links."""
        self.logger.info("Verifying E-Services Section...")
        if self.is_visible(self.header_eservices):
            self.logger.info("E-Services Header found.")
            if self.is_visible(self.link_eservices_apply) and self.is_visible(self.link_eservices_requests):
                self.logger.info("E-Services 'Apply' and 'My Requests' links found.")
                return True
        self.logger.error("E-Services section missing or incomplete.")
        return False

    def verify_payment_status(self):
        """Verifies the Payment Status section exists and has history link."""
        self.logger.info("Verifying Payment Status Section...")
        if self.is_visible(self.header_payment_status):
            self.logger.info("Payment Status Header found.")
            if self.is_visible(self.link_payment_history):
                self.logger.info("Payment History link found.")
                return True
        self.logger.error("Payment Status section missing or incomplete.")
        return False

    def verify_workflow(self):
        """Verifies Registration Steps sidebar and Recent Activities."""
        self.logger.info("Verifying Workflow / Registration Steps...")
        steps_found = self.is_visible(self.header_reg_steps)
        activities_found = self.is_visible(self.header_recent_activities)
        
        if steps_found and activities_found:
             self.logger.info("Registration Steps and Recent Activities found.")
             return True
        
        self.logger.error(f"Workflow sections missing. Steps: {steps_found}, Activities: {activities_found}")
        return False

    def do_logout(self):
        """Performs logout."""
        self.logger.info("Attempting Logout...")
        try:
            self.do_click(self.dropdown_user)
            self.do_click(self.link_logout)
            self.logger.info("Logout clicked.")
            return True
        except Exception as e:
            self.logger.error(f"Logout failed: {e}")
            return False
