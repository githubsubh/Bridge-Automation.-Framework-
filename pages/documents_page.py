from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import time

class DocumentsPage(BasePage):
    # Updated Locators from Dashboard view
    PHOTO_INPUT = (By.ID, "documentuploadform-photo")
    SIGNATURE_INPUT = (By.ID, "documentuploadform-signature")
    BED_INPUT = (By.ID, "documentuploadform-bed_certificate")
    APPOINTMENT_INPUT = (By.ID, "documentuploadform-appointment_letter")
    SELF_DECLARATION_INPUT = (By.ID, "documentuploadform-self_declaration")
    
    BTN_UPLOAD_SUBMIT = (By.ID, "uploadSubmitv1")
    BTN_VIEW_SAMPLES = (By.CLASS_NAME, "sample-docv")

    def upload_all_documents(self, photo_path, doc_path):
        """
        Dynamically find file inputs and upload appropriate files based on labels/context.
        """
        file_inputs = self.driver.find_elements(By.XPATH, "//input[@type='file']")
        self.logger.info(f"Found {len(file_inputs)} file inputs.")
        
        for inp in file_inputs:
            try:
                # Try to find a label or preceding text
                # Strategy: Check parent text or nearby label
                # Getting parent text often works for form groups
                parent = inp.find_element(By.XPATH, "./.. | ./../..")
                text = parent.text.lower()
                
                # Also check 'id' or 'name' as fallback hint
                eid = inp.get_attribute("id") or ""
                name = inp.get_attribute("name") or ""
                combined_text = (text + eid + name).lower()
                
                target_file = doc_path # Default to PDF
                
                if "photo" in combined_text or "image" in combined_text:
                    target_file = photo_path
                elif "signature" in combined_text:
                    target_file = photo_path # Signature usually image
                    
                self.logger.info(f"Uploading to input (ID='{eid}'): {target_file}")
                inp.send_keys(target_file)
                time.sleep(0.3)
                
            except Exception as e:
                self.logger.error(f"Failed to upload to an input: {e}")

    def toggle_checkboxes(self):
        """Find and click all checkboxes on the page if not already selected."""
        checkboxes = self.driver.find_elements(By.XPATH, "//input[@type='checkbox']")
        self.logger.info(f"Found {len(checkboxes)} checkboxes.")
        for cb in checkboxes:
            try:
                if not cb.is_selected():
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", cb)
                    self.driver.execute_script("arguments[0].click();", cb)
                    self.logger.info("Toggled a checkbox")
            except Exception as e:
                self.logger.warning(f"Could not toggle checkbox: {e}")

    def click_save_continue(self):
        """Click the Save & Continue button using a robust locator."""
        # The ID 'submitbtnv' was verified in debug logs
        try:
            self.logger.info("Clicking Save & Continue using ID 'submitbtnv'")
            self.do_click((By.ID, "submitbtnv"))
        except Exception as e:
            self.logger.warning(f"ID click failed: {e}. Trying text-based fallback.")
            try:
                # Try finding button by text (Save & Continue)
                btn = self.driver.find_element(By.XPATH, "//button[contains(., 'Save') and contains(., 'Continue')]")
                self.driver.execute_script("arguments[0].click();", btn)
                self.logger.info("Clicked Save & Continue using text and JS")
            except:
                 # Last resort: generic type='submit'
                 self.logger.warning("Text click failed. Trying generic submit button.")
                 self.do_click((By.XPATH, "//button[@type='submit']"))

    def verify_documents_displayed(self):
        """Verifies that the main document fields are visible."""
        self.logger.info("Checking visibility of document fields...")
        photo = self.is_visible(self.PHOTO_INPUT)
        sig = self.is_visible(self.SIGNATURE_INPUT)
        bed = self.is_visible(self.BED_INPUT)
        
        if photo and sig and bed:
            self.logger.info("Core document fields are visible.")
            return True
        self.logger.error(f"Some fields missing. Photo: {photo}, Sig: {sig}, BEd: {bed}")
        return False

    def click_sample_document(self):
        """Clicks the first 'View Sample Document' button."""
        self.logger.info("Attempting to click a sample document link...")
        samples = self.driver.find_elements(*self.BTN_VIEW_SAMPLES)
        if samples:
            self.driver.execute_script("arguments[0].click();", samples[0])
            self.logger.info("Clicked first sample document.")
            return True
        self.logger.warning("No sample document links found.")
        return False
    def upload_dashboard_documents(self, photo_path, doc_path):
        """Uploads documents using specific dashboard view locators, enabling them via JS if needed."""
        self.logger.info("Uploading documents in Dashboard 'My Documents' view...")
        
        doc_map = {
            "Photo": (self.PHOTO_INPUT, photo_path),
            "Signature": (self.SIGNATURE_INPUT, photo_path),
            "B.Ed Certificate": (self.BED_INPUT, doc_path),
            "Appointment Letter": (self.APPOINTMENT_INPUT, doc_path),
            "Self Declaration": (self.SELF_DECLARATION_INPUT, doc_path)
        }

        for label, (locator, path) in doc_map.items():
            try:
                # Force enable the input if it's disabled
                elem = self.get_element(locator)
                if not elem.is_enabled():
                    self.logger.info(f"Input for {label} is disabled. Enabling via JavaScript...")
                    self.driver.execute_script("arguments[0].removeAttribute('disabled');", elem)
                
                elem.send_keys(path)
                self.logger.info(f"Uploaded {label}: {path}")
                time.sleep(0.5)
            except Exception as e:
                self.logger.warning(f"Could not upload {label}: {e}")

    def click_upload_submit(self):
        """Clicks the upload/submit button, using JS if intercepted."""
        self.logger.info("Clicking Upload Submit button...")
        try:
            # Scroll to element first
            elem = self.get_element(self.BTN_UPLOAD_SUBMIT)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
            time.sleep(1)
            self.do_click(self.BTN_UPLOAD_SUBMIT)
        except Exception as e:
            self.logger.warning(f"Standard click failed: {e}. Attempting JS click...")
            try:
                elem = self.get_element(self.BTN_UPLOAD_SUBMIT)
                self.driver.execute_script("arguments[0].click();", elem)
                self.logger.info("Clicked Submit via JavaScript.")
            except Exception as e2:
                self.logger.error(f"JS click also failed: {e2}")
