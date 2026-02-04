from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import time

class DocumentsPage(BasePage):
    # Locators
    # Assuming IDs for file inputs
    PHOTO_INPUT = (By.ID, "file_photo")
    SIGNATURE_INPUT = (By.ID, "file_signature")
    AADHAR_INPUT = (By.ID, "file_aadhar")
    TENTH_INPUT = (By.ID, "file_10th")
    TWELFTH_INPUT = (By.ID, "file_12th")
    
    CHECKBOX_1 = (By.ID, "confirm_no_change")
    CHECKBOX_2 = (By.ID, "undertaking") 
    
    SAVE_CONTINUE_BTN = (By.ID, "btn_save_continue_docs")

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
                time.sleep(1)
                
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

    def debug_print_ids(self):
        import time
        self.logger.info("--- DEBUGGING DOCUMENTS PAGE LOCATORS ---")
        time.sleep(2)
        elements = self.driver.find_elements(By.XPATH, "//*[@id]")
        for elem in elements:
            try:
                eid = elem.get_attribute("id")
                tag = elem.tag_name
                etype = elem.get_attribute("type")
                if eid and ("file" in eid.lower() or "doc" in eid.lower() or "btn" in eid.lower() or "check" in eid.lower()):
                     self.logger.info(f"Relevant Document Element: ID='{eid}', Tag='{tag}', Type='{etype}'")
            except:
                pass
        self.logger.info("--- END DEBUGGING ---")
