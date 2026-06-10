from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    
    # School & Regional Centre Modal (from DOM)
    btn_school_details = (By.CSS_SELECTOR, "button[data-bs-target='#SchoolNIOSRegionalCentreDetailsModal']")
    modal_school_details = (By.ID, "SchoolNIOSRegionalCentreDetailsModal")
    modal_close_btn = (By.CSS_SELECTOR, "#SchoolNIOSRegionalCentreDetailsModal .btn-close")
    header_school_details_modal = (By.XPATH, "//h6[contains(text(), 'School Details')]")
    header_regional_centre_modal = (By.XPATH, "//h6[contains(text(), 'Regional Centre Details')]")
    
    # Progress Items / Sidebar (from DOM)
    container_reg_steps = (By.CSS_SELECTOR, ".list-group.list-group-flush.mt-1")
    badges_success = (By.CSS_SELECTOR, ".badge.bg-success")
    progress_bar = (By.CSS_SELECTOR, ".progress-bar")
    
    # Teacher Info
    text_teacher_name = (By.CSS_SELECTOR, ".cname")
    text_reference_no = (By.XPATH, "//strong[contains(text(), 'Reference No.:')]/parent::p")
    text_udise_code = (By.XPATH, "//th[contains(text(), 'UDISE Code')]/parent::tr/parent::thead/parent::table/tbody/tr[1]/td[1]")

    # Header & Logout
    dropdown_user = (By.ID, "dropdownMenuLink")
    link_change_password = (By.XPATH, "//a[@href='/teacher/change-password']")
    link_logout = (By.XPATH, "//a[@href='/auth/logout']")

    def __init__(self, driver):
        super().__init__(driver)

    def get_teacher_name(self):
        return self.get_element_text(self.text_teacher_name).strip()

    def get_reference_no(self):
        full_text = self.get_element_text(self.text_reference_no)
        # Assuming format like "Reference No.: V1125000043"
        if ":" in full_text:
            return full_text.split(":")[1].strip()
        return full_text.strip()

    def get_modal_udise_code(self):
        return self.get_element_text(self.text_udise_code).strip()

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

    def click_school_details(self):
        """Clicks the School & Regional Centre Details button."""
        self.logger.info("Opening School & NIOS Regional Centre Details Modal...")
        self.do_click(self.btn_school_details)

    def verify_modal_content(self):
        """Verifies tables inside the school details modal and closes it."""
        import time
        try:
            # Wait for modal to be fully visible
            time.sleep(2)
            self.logger.info("Verifying Modal headers...")
            s_header = self.is_visible(self.header_school_details_modal)
            r_header = self.is_visible(self.header_regional_centre_modal)
            
            if s_header and r_header:
                self.logger.info("School and Regional Centre information visible in modal.")
                
                # Scrape school name for logging (2nd TD in the first table body)
                school_name = self.get_element_text((By.XPATH, "//div[@id='SchoolNIOSRegionalCentreDetailsModal']//tbody/tr[1]/td[2]"))
                self.logger.info(f"Modal Audit Success: Found School - {school_name}")
                
                # Close Modal
                self.do_click(self.modal_close_btn)
                self.logger.info("Modal closed.")
                return True
        except Exception as e:
            self.logger.error(f"Modal verification failed: {e}")
        return False

    def audit_sidebar_progress(self):
        """Audits the sidebar to ensure all 5 registration steps have success checkmarks."""
        self.logger.info("Auditing Sidebar Registration Steps via DOM structure...")
        
        # Verify 100% progress bar
        try:
            p_bar = self.get_element(self.progress_bar)
            progress_text = p_bar.text.strip()
            self.logger.info(f"Progress bar value: {progress_text}")
        except:
            progress_text = "0%"

        success_badges = self.driver.find_elements(*self.badges_success)
        self.logger.info(f"Number of green checkmarks found: {len(success_badges)}")
        
        return len(success_badges) == 5 and "100%" in progress_text

    def do_logout(self):
        """Performs logout with deliberate pauses for visibility."""
        self.logger.info("Attempting Logout...")
        try:
            self.do_click(self.dropdown_user)
            # Wait for logout link to be visible
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.link_logout))
            self.logger.info("Logout link appeared. Waiting 3 seconds...")
            import time
            time.sleep(3)
            
            self.do_click(self.link_logout)
            self.logger.info("Logout clicked. Waiting 2 seconds for redirection...")
            time.sleep(2)
            return True
        except Exception as e:
            self.logger.error(f"Logout failed: {e}")
            return False
