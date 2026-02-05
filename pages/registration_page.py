from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import Select

class RegistrationPage(BasePage):
    # Locators
    textbox_name_id = (By.ID, "basicdetailform-name")
    textbox_mother_name_id = (By.ID, "basicdetailform-mother_name")
    textbox_father_name_id = (By.ID, "basicdetailform-father_name")
    textbox_dob_id = (By.ID, "basicdetailform-date_of_birth")
    dropdown_gender_id = (By.ID, "basicdetailform-gender")
    textbox_udise_code_id = (By.ID, "basicdetailform-udise_code")
    textbox_teacher_id_id = (By.ID, "basicdetailform-teacher_id")
    button_submit_id = (By.ID, "submit-basic-details")
    button_verify_id = (By.ID, "verify-udise")

    def __init__(self, driver):
        super().__init__(driver)

    def set_name(self, name):
        self.do_send_keys(self.textbox_name_id, name)
        
    def set_mother_name(self, mname):
        self.do_send_keys(self.textbox_mother_name_id, mname)
        
    def set_father_name(self, fname):
        self.do_send_keys(self.textbox_father_name_id, fname)
        
    def set_dob(self, dob):
        # Use JavaScript to set the date to avoid input mask issues
        element = self.driver.find_element(*self.textbox_dob_id)
        self.driver.execute_script("arguments[0].value = arguments[1];", element, dob)
        # Trigger change event just in case
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", element)
        self.logger.info(f"Set DOB to '{dob}' using JavaScript")
        
    def set_gender(self, gender):
        # Handle Chosen dropdown
        try:
            # Click the Chosen container to open dropdown
            self.do_click((By.ID, "basicdetailform_gender_chosen"))
            # Find the option with text and click
            # Options are usually in li tags under ul.chosen-results
            xpath = f"//div[@id='basicdetailform_gender_chosen']//ul[@class='chosen-results']/li[contains(text(), '{gender}')]"
            self.do_click((By.XPATH, xpath))
            self.logger.info(f"Selected gender: {gender}")
        except Exception as e:
            self.logger.error(f"Failed to select gender '{gender}': {e}")
            raise

    def set_udise_code(self, udise):
        self.do_send_keys(self.textbox_udise_code_id, udise)
        
    def check_verification_success(self):
        # Check for success message or green badge
        pass 

    def handle_modal(self, timeout=1):
        try:
            # Very short check for modal
            self.logger.info(f"Quick check for modal (timeout={timeout}s)...")
            from selenium.webdriver.support.wait import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            confirm_btn = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.swal2-confirm"))
            )
            confirm_btn.click()
            self.logger.info("Dismissed modal")
            time.sleep(0.5)
        except Exception:
            pass

    def click_continue(self):
        """Click the 'Continue' button on Basic Details page."""
        try:
            # Quick modal check before clicking
            self.handle_modal(timeout=1)
            
            selector = (By.ID, "submit-basic-details")
            
            # Wait only briefly for button to be enabled (max 2s)
            import time
            for _ in range(2):
                btn = self.driver.find_element(*selector)
                if btn.is_enabled() and "disabled" not in btn.get_attribute("outerHTML"):
                    break
                time.sleep(1)
            
            self.logger.info("Screen waiting: 5 seconds pause as per user preference...")
            time.sleep(5)
            
            self.do_click(selector)
            self.logger.info("Clicked Continue button")
        except Exception as e:
            self.logger.warning(f"Click failed: {e}")
            try:
                element = self.driver.find_element(By.ID, "submit-basic-details")
                self.driver.execute_script("arguments[0].click();", element)
            except Exception:
                raise
            
    def click_verify_udise(self):
        self.do_click(self.button_verify_id)

    def click_submit(self):
        self.do_click(self.button_submit_id)
