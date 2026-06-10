import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.registration_page import RegistrationPage
from pages.authentication_page import AuthenticationPage
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen
from utilities.data_utils import DataUtils

class Test_US05_Registration_Stage2:
    base_url = ReadConfig.getApplicationURL()
    logger = LogGen.loggen()

    def reach_authentication_page(self, driver):
        """Helper to navigate through Stage 1 to reach Stage 2 (Authentication)"""
        driver.get(self.base_url)
        reg_page = RegistrationPage(driver)
        
        reg_page.handle_modal(timeout=3)
        reg_page.wait_for_form()
        
        # Fill Stage 1 with valid data
        reg_page.set_name(DataUtils.get_random_name())
        reg_page.set_father_name("Father Name")
        reg_page.set_mother_name("Mother Name")
        reg_page.set_dob("01-01-1990")
        reg_page.set_gender("Male")
        reg_page.set_udise_code("10101000101")
        
        try:
            reg_page.click_verify_udise()
            time.sleep(1)
        except: pass
        
        reg_page.click_continue()
        
        # Wait for either Eligibility or Authentication
        WebDriverWait(driver, 10).until(
            lambda d: "eligibility" in d.current_url or "authentication" in d.current_url
        )
        
        # In case Eligibility is before Auth in this environment
        if "eligibility" in driver.current_url:
            try:
                driver.find_element(By.ID, "eligibility-date_of_appointment").send_keys("01-01-2022")
                driver.find_element(By.ID, "submit-eligibility").click()
            except: pass
            
        WebDriverWait(driver, 10).until(EC.url_contains("authentication"))

    @pytest.mark.regression
    def test_tc_us05_01_invalid_email(self, setup):
        """TC_US05_01: Verify invalid email format validation"""
        self.logger.info("**** Starting TC_US05_01: Invalid Email Format ****")
        driver = setup
        self.reach_authentication_page(driver)
        
        auth_page = AuthenticationPage(driver)
        auth_page.set_email("user@abc") # Invalid format
        auth_page.set_mobile("9999999999")
        auth_page.click_submit()
        
        time.sleep(2)
        error_elements = driver.find_elements(
            By.XPATH,
            "//*[contains(@class,'help-block') or contains(@class,'invalid-feedback')]"
        )
        all_errors = " ".join([e.text for e in error_elements if e.text]).lower()
        
        if not any(word in all_errors for word in ["email", "valid", "format"]):
            self.logger.warning("BUG: Email format validation NOT enforced.")
            pytest.fail("BUG: Email format validation is missing.")
        else:
            self.logger.info("Email validation successful.")

    @pytest.mark.regression
    def test_tc_us05_02_mobile_length(self, setup):
        """TC_US05_02: Verify mobile number length validation"""
        self.logger.info("**** Starting TC_US05_02: Mobile Length Validation ****")
        driver = setup
        self.reach_authentication_page(driver)
        
        auth_page = AuthenticationPage(driver)
        auth_page.set_email(DataUtils.generate_email_incremental())
        auth_page.set_mobile("987654") # Less than 10 digits
        auth_page.click_submit()
        
        time.sleep(2)
        error_elements = driver.find_elements(
            By.XPATH,
            "//*[contains(@class,'help-block') or contains(@class,'invalid-feedback')]"
        )
        all_errors = " ".join([e.text for e in error_elements if e.text]).lower()
        
        if "10" not in all_errors and "digit" not in all_errors and "valid" not in all_errors:
            self.logger.warning("BUG: Mobile length validation NOT enforced.")
            pytest.fail("BUG: Mobile length validation is missing.")
        else:
            self.logger.info("Mobile length validation successful.")
