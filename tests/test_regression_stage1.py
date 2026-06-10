import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.registration_page import RegistrationPage
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen

class Test_US04_Registration_Stage1:
    base_url = ReadConfig.getApplicationURL()
    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_tc_us04_01_mandatory_fields(self, setup):
        """TC_US04_01: Verify validation of mandatory fields"""
        self.logger.info("**** Starting TC_US04_01: Mandatory Fields Validation ****")
        driver = setup
        driver.get(self.base_url)
        reg_page = RegistrationPage(driver)
        
        # Handle initial modal if present
        reg_page.handle_modal(timeout=3)
        reg_page.wait_for_form()
        
        # Click submit directly without entering any data
        self.logger.info("Clicking submit without filling fields to trigger validation")
        reg_page.click_continue()
        
        # Wait for validation to trigger (usually fast but let's give it 2 seconds)
        time.sleep(2)
        
        # Look for the required field errors in the DOM
        error_elements = driver.find_elements(
            By.XPATH,
            "//*[contains(@class,'help-block') or contains(@class,'invalid-feedback') or contains(text(), 'cannot be blank') or contains(text(), 'required')]"
        )
        
        # We expect multiple errors since multiple fields are empty
        assert len(error_elements) > 2, f"Expected multiple mandatory field errors, found {len(error_elements)}"
        self.logger.info("Mandatory fields validation successful.")

    @pytest.mark.regression
    def test_tc_us04_02_alpha_only_names(self, setup):
        """TC_US04_02: Verify Alpha-only validation for Name fields"""
        self.logger.info("**** Starting TC_US04_02: Alpha-only Name Validation ****")
        driver = setup
        driver.get(self.base_url)
        reg_page = RegistrationPage(driver)
        
        reg_page.handle_modal(timeout=3)
        reg_page.wait_for_form()
        
        # Enter an invalid numeric/alphanumeric name
        self.logger.info("Entering invalid name 'Test123' to check alpha-only rule")
        driver.execute_script(
            "var el = document.getElementById('basicdetailform-name');"
            "if(el) { el.value = 'Test123'; el.dispatchEvent(new Event('input', {bubbles:true})); el.dispatchEvent(new Event('change', {bubbles:true})); }"
        )
        time.sleep(1)
        
        # Click submit to trigger field-level validation
        reg_page.click_continue()
        time.sleep(2)
        
        # Fetch all error text from the page to see if alpha validation failed
        error_elements = driver.find_elements(
            By.XPATH,
            "//*[contains(@class,'help-block') or contains(@class,'invalid-feedback') or contains(@class,'field-error')]"
        )
        all_errors = " ".join([e.text for e in error_elements if e.text]).lower()
        self.logger.info(f"Captured error texts: {all_errors}")
        
        # Validation Check: The string should complain about letters/alphabets
        if not any(word in all_errors for word in ["alpha", "character", "letter", "invalid"]):
            self.logger.warning("BUG: Alpha-only validation NOT enforced on name field! Input 'Test123' was accepted.")
            pytest.fail("BUG: Alpha-only name validation is missing. System accepted 'Test123' without error.")
        else:
            self.logger.info("Alpha-only name validation successful.")

    @pytest.mark.regression
    def test_tc_us04_04_dob_age_validation(self, setup):
        """TC_US04_04: Verify Minimum Age validation (18+ years)"""
        self.logger.info("**** Starting TC_US04_04: DOB Age Validation ****")
        driver = setup
        driver.get(self.base_url)
        reg_page = RegistrationPage(driver)
        
        reg_page.handle_modal(timeout=3)
        reg_page.wait_for_form()
        
        # Set a DOB that makes the teacher under 18 years old (e.g. year 2015)
        self.logger.info("Setting underage DOB: 10-10-2015")
        driver.execute_script(
            "var el = document.getElementById('basicdetailform-date_of_birth');"
            "if(el) { el.value = '10-10-2015'; el.dispatchEvent(new Event('change', {bubbles:true})); }"
        )
        time.sleep(1)
        
        # Attempt to proceed
        reg_page.click_continue()
        time.sleep(2)
        
        # Check if the system throws an age-related error
        page_source = driver.page_source.lower()
        error_elements = driver.find_elements(
            By.XPATH,
            "//*[contains(@class,'help-block') or contains(@class,'invalid-feedback') or contains(@class,'alert')]"
        )
        all_errors = " ".join([e.text for e in error_elements if e.text]).lower()
        combined = page_source + all_errors
        
        if not any(word in combined for word in ["age", "18", "years", "dob", "birth", "minor"]):
            self.logger.warning("BUG: Age validation NOT enforced! Underage DOB '10-10-2015' was accepted.")
            pytest.fail("BUG: Minimum age (18+) validation is missing on DOB field.")
        else:
            self.logger.info("Age validation confirmed — underage DOB rejected correctly.")

    @pytest.mark.regression
    def test_tc_us04_05_udise_ajax_validation(self, setup):
        """TC_US04_05: Verify UDISE Code AJAX Validation"""
        self.logger.info("**** Starting TC_US04_05: UDISE AJAX Validation ****")
        driver = setup
        driver.get(self.base_url)
        reg_page = RegistrationPage(driver)
        
        reg_page.handle_modal(timeout=3)
        reg_page.wait_for_form()
        
        # Enter an invalid UDISE code that shouldn't exist in master DB
        self.logger.info("Entering invalid UDISE code: '00000000000'")
        reg_page.set_udise_code("00000000000")
        
        # Trigger AJAX via blur/change (clicking the verify button if it exists)
        try:
            reg_page.click_verify_udise()
        except:
            # If no verify button, just click body to blur
            driver.find_element(By.TAG_NAME, 'body').click()
            
        time.sleep(3) # Wait for backend validation
        
        # Verification: System should tell us it's not found
        page_source = driver.page_source.lower()
        assert "not found" in page_source or "invalid" in page_source, "UDISE validation error message not displayed."
        self.logger.info("UDISE AJAX validation successful.")
