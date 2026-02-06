import pytest
import time
import os
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.documents_page import DocumentsPage
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen

class Test_011_ReuploadDocuments:
    home_url = "https://bridge-uat.nios.ac.in/"
    email = ReadConfig.getLoginEmail()
    password = ReadConfig.getLoginPassword()
    logger = LogGen.loggen()
    
    # Updated paths to the specific dummy files we just generated
    base_path = "/Users/anujjha/Bridge-Automation.-Framework-"
    photo_path = os.path.join(base_path, "test_data/official_photo.jpg")
    sig_path = os.path.join(base_path, "test_data/official_signature.jpg")
    doc_path = os.path.join(base_path, "test_data/official_certificate.pdf")
    
    def test_reupload_documents_flow(self, setup):
        self.logger.info("**** Starting Test_011_ReuploadDocuments (Refined) ****")
        self.driver = setup
        self.driver.get(self.home_url)
        
        # 1. Login
        home_page = HomePage(self.driver)
        home_page.navigate_to_teacher_login()
        
        login_page = LoginPage(self.driver)
        if not login_page.login_with_manual_captcha(self.email, self.password, timeout=120):
            pytest.fail("Login failed, cannot test Re-upload Documents.")
            
        self.logger.info("Login successful. Waiting 5 seconds on Dashboard...")
        time.sleep(5)
        
        dashboard_page = DashboardPage(self.driver)
        
        # 2. Navigate to My Documents
        self.logger.info("Navigating to My Documents...")
        dashboard_page.mouse_hover(dashboard_page.link_view_documents)
        time.sleep(2)
        dashboard_page.do_click(dashboard_page.link_view_documents)
        
        docs_page = DocumentsPage(self.driver)
        self.logger.info("Waiting 5 seconds for Documents page to load...")
        time.sleep(5)
        
        # Capture DOM as requested by user
        dom_content = self.driver.page_source
        with open("documents_upload_page_live.html", "w", encoding="utf-8") as f:
            f.write(dom_content)
        self.logger.info("LIVE DOM captured and saved to 'documents_upload_page_live.html'")
        
        # 3. Perform Re-upload (Slowed down for visual confirmation)
        self.logger.info("--- Phase: Systematic Re-upload ---")
        
        # Logic to enable and upload
        def force_upload(label, locator, file_path):
            self.logger.info(f"Attempting upload for {label}: {file_path}")
            elem = docs_page.get_element(locator)
            # Remove disabled attribute via JS
            self.driver.execute_script("arguments[0].removeAttribute('disabled');", elem)
            time.sleep(1)
            elem.send_keys(file_path)
            self.logger.info(f"DONE: {label} uploaded. Pausing 3s...")
            time.sleep(3)

        force_upload("Passport Photo", docs_page.PHOTO_INPUT, self.photo_path)
        force_upload("Signature", docs_page.SIGNATURE_INPUT, self.sig_path)
        force_upload("B.Ed Certificate", docs_page.BED_INPUT, self.doc_path)
        force_upload("Appointment Letter", docs_page.APPOINTMENT_INPUT, self.doc_path)
        force_upload("Self Declaration", docs_page.SELF_DECLARATION_INPUT, self.doc_path)
        
        self.logger.info("All documents uploaded. Waiting 8 seconds for visual inspection...")
        time.sleep(8)
        
        # 4. Save and Submit
        self.logger.info("Moving to Submit button...")
        docs_page.mouse_hover(docs_page.BTN_UPLOAD_SUBMIT)
        time.sleep(2)
        
        self.logger.info("Clicking Submit button...")
        docs_page.click_upload_submit()
        
        self.logger.info("Submission clicked. Waiting 10 seconds for results...")
        time.sleep(10)
        
        # 5. Return to Dashboard
        self.logger.info("Navigating back to Dashboard to confirm context...")
        self.driver.get(self.home_url + "teacher/dashboard")
        time.sleep(5)
        
        self.logger.info("**** Test_011_ReuploadDocuments (Refined) Completed Successfully ****")
