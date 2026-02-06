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
    
    # My Documents
    header_my_documents = (By.XPATH, "//h6[contains(text(), 'My Documents')]")
    link_view_documents = (By.XPATH, "//a[@href='/teacher/documents']")
    
    # Print
    header_print = (By.XPATH, "//h6[contains(text(), 'Print')]")
    link_print_application = (By.XPATH, "//a[@href='/teacher/print-application-form']")
    
    # Results
    header_results = (By.XPATH, "//h6[contains(text(), 'Results')]")
    link_public_exam_results = (By.XPATH, "//a[contains(text(), 'Public Exam Results')]")
    
    # Grievances
    header_grievances = (By.XPATH, "//h6[contains(text(), 'Grievances')]")
    link_submit_grievance = (By.XPATH, "//a[@href='https://grs.nios.ac.in/']")
    
    # Header & Logout
    dropdown_user = (By.ID, "dropdownMenuLink")
    link_change_password = (By.XPATH, "//a[@href='/teacher/change-password']")
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

    def verify_my_documents(self):
        """Verifies the My Documents section exists and has View Documents link."""
        self.logger.info("Verifying My Documents Section...")
        if self.is_visible(self.header_my_documents):
             if self.is_visible(self.link_view_documents):
                 self.logger.info("My Documents section verified.")
                 return True
        self.logger.error("My Documents section missing or incomplete.")
        return False

    def verify_print_section(self):
        """Verifies the Print section exists and has Application Form link."""
        self.logger.info("Verifying Print Section...")
        if self.is_visible(self.header_print):
             if self.is_visible(self.link_print_application):
                 self.logger.info("Print section verified.")
                 return True
        self.logger.error("Print section missing or incomplete.")
        return False

    def verify_results_section(self):
        """Verifies the Results section exists."""
        self.logger.info("Verifying Results Section...")
        if self.is_visible(self.header_results):
             if self.is_visible(self.link_public_exam_results):
                 self.logger.info("Results section verified.")
                 return True
        self.logger.error("Results section missing or incomplete.")
        return False

    def verify_grievances_section(self):
        """Verifies the Grievances section exists."""
        self.logger.info("Verifying Grievances Section...")
        if self.is_visible(self.header_grievances):
             if self.is_visible(self.link_submit_grievance):
                 self.logger.info("Grievances section verified.")
                 return True
        self.logger.error("Grievances section missing or incomplete.")
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
