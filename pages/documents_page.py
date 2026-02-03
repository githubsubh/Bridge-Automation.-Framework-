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

    def upload_document(self, doc_type, file_path):
        locator = None
        if doc_type == "photo":
            locator = self.PHOTO_INPUT
        elif doc_type == "signature":
            locator = self.SIGNATURE_INPUT
        elif doc_type == "aadhar":
            locator = self.AADHAR_INPUT
        elif doc_type == "10th":
            locator = self.TENTH_INPUT
        elif doc_type == "12th":
            locator = self.TWELFTH_INPUT
            
        if locator:
            # Send keys to file input directly
            self.driver.find_element(*locator).send_keys(file_path)
            self.logger.info(f"Uploaded {doc_type} from {file_path}")
            time.sleep(1) # Wait for upload

    def toggle_checkboxes(self):
        # Click known checkboxes
        try:
            self.do_click(self.CHECKBOX_1)
        except:
            self.logger.warning("Could not click Checkbox 1 by ID")
            
        try:
            self.do_click(self.CHECKBOX_2)
        except:
            self.logger.warning("Could not click Checkbox 2 by ID")
            
        # Fallback: Click all unchecked checkboxes
        checkboxes = self.driver.find_elements(By.XPATH, "//input[@type='checkbox']")
        for cb in checkboxes:
            if not cb.is_selected():
                try:
                    cb.click()
                except:
                    self.driver.execute_script("arguments[0].click();", cb)

    def click_save_continue(self):
        self.do_click(self.SAVE_CONTINUE_BTN)
