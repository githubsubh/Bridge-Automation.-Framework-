import pytest
import time
from pages.registration_page import RegistrationPage
from pages.eligibility_page import EligibilityPage
from pages.authentication_page import AuthenticationPage
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen
from utilities.data_utils import DataUtils
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Test_009_Registration_Negative:
    baseURL = ReadConfig.getApplicationURL()
    logger = LogGen.loggen()
    timeouts = ReadConfig.getTimeouts()

    def fill_step1_basic_details(self, driver):
        """Helper to fill Step 1 with valid data."""
        reg_page = RegistrationPage(driver)
        reg_page.handle_modal()
        
        name = DataUtils.get_random_name()
        reg_page.set_name(name)
        reg_page.set_father_name("Father " + name)
        reg_page.set_mother_name("Mother " + name)
        reg_page.set_dob(DataUtils.get_random_dob())
        reg_page.set_gender("Male")
        reg_page.set_udise_code("10101000101")
        reg_page.click_verify_udise()
        reg_page.handle_modal()
        reg_page.click_continue()
        
        # Verify navigation to Step 2
        try:
            WebDriverWait(driver, 10).until(EC.url_contains("eligibility"))
            self.logger.info("Successfully navigated to Eligibility Step.")
        except:
            self.logger.error("Failed to navigate to Eligibility step in setup helper.")
            raise

    def fill_step2_eligibility(self, driver):
        """Helper to fill Step 2 with valid data."""
        elig_page = EligibilityPage(driver)
        try:
            elig_page.set_date_of_appointment("01-01-2022")
            elig_page.click_continue()
            
            # Verify navigation to Step 3
            WebDriverWait(driver, 10).until(EC.url_contains("authentication"))
            self.logger.info("Successfully navigated to Authentication Step.")
        except Exception as e:
            self.logger.warning(f"Eligibility step issue: {e}")
            # Sometimes eligibility is skipped or pre-filled

    def test_basic_details_validation_traversal(self, setup):
        """
        Scenario: Sequentially test validation on Basic Details page without reloading.
        1. Empty Submission.
        2. Invalid Name (Numeric).
        3. Same Name for Father and Mother.
        4. Invalid UDISE Code.
        """
        self.logger.info("**** Starting Negative Test: Basic Details Traversal ****")
        self.driver = setup
        self.driver.get(self.baseURL)
        reg_page = RegistrationPage(self.driver)
        reg_page.handle_modal()
        
        # --- 1. Empty Submission ---
        self.logger.info(">>> Check 1: Empty Submission")
        reg_page.click_continue()
        time.sleep(2)
        
        if "eligibility" in self.driver.current_url.lower():
            self.logger.error("FAILED: Empty submission allowed.")
            assert False
        else:
            self.logger.info("PASSED: Empty submission blocked.")
            time.sleep(2) # Wait after warning message
            
        # --- 2. Invalid Name (Numeric) ---
        self.logger.info(">>> Check 2: Invalid Name (Numeric)")
        reg_page.set_name("Tester123")
        # Fill others validly to isolate Name error
        reg_page.set_father_name("Father Valid")
        reg_page.set_mother_name("Mother Valid")
        reg_page.set_dob("01-01-1990")
        reg_page.set_gender("Male")
        reg_page.set_udise_code("10101000101")
        reg_page.click_verify_udise()
        reg_page.handle_modal(timeout=2)
        
        reg_page.click_continue()
        time.sleep(2)
        
        if "eligibility" in self.driver.current_url.lower():
            self.logger.error("FAILED: Numeric Name accepted.")
            assert False
        else:
            self.logger.info("PASSED: Numeric Name blocked.")
            time.sleep(2) # Wait after warning message
            
        # Fix Name for next step
        reg_page.set_name("Valid Name")
        
        # --- 3. Same Parent Names ---
        self.logger.info(">>> Check 3: Same Father and Mother Name")
        parent_name = "Same Parent"
        reg_page.set_father_name(parent_name)
        reg_page.set_mother_name(parent_name)
        
        reg_page.click_continue()
        time.sleep(2)
        
        if "eligibility" in self.driver.current_url.lower():
             self.logger.error("FAILED: Same parent names accepted.")
             assert False
        else:
             self.logger.info("PASSED: Same parent names blocked.")
             time.sleep(2) # Wait after warning message
             
        # Fix Parents for next step
        reg_page.set_father_name("Father Valid")
        reg_page.set_mother_name("Mother Valid")
        
        # --- 4. Invalid UDISE Code ---
        self.logger.info(">>> Check 4: Invalid UDISE Code")
        # Enter wrong code
        reg_page.set_udise_code("0000") # Too short
        reg_page.click_verify_udise()
        time.sleep(2)
        
        # Check for alert or error
        try:
            alert = self.driver.switch_to.alert
            txt = alert.text
            self.logger.info(f"Alert captured: {txt}")
            alert.accept()
            self.logger.info("PASSED: Invalid UDISE triggered alert.")
            time.sleep(2) # Wait after warning message
        except:
            # Check for invalid class or error message
            if len(self.driver.find_elements(By.CSS_SELECTOR, ".field-validation-error")) > 0:
                 self.logger.info("PASSED: Invalid UDISE validation error found.")
                 time.sleep(2) # Wait after warning message
            else:
                 # Attempt continue to see if blocked
                 reg_page.click_continue()
                 time.sleep(1)
                 if "eligibility" in self.driver.current_url.lower():
                     self.logger.error("FAILED: Invalid UDISE accepted.")
                     assert False
                 else:
                     self.logger.info("PASSED: Invalid UDISE blocked submission.")
                     time.sleep(2) # Wait after warning message

        # Fix UDISE for next step
        reg_page.set_udise_code("10101000101")
        time.sleep(1)
        reg_page.click_verify_udise()
        # Handle modal if it appears after verification
        reg_page.handle_modal(timeout=2)
        
        # --- 5. Invalid DOB ---
        self.logger.info(">>> Check 5: Invalid Date of Birth")
        # Trying a logically invalid date "32-13-2022"
        self.logger.info("Setting Invalid DOB: 32-13-2022 (Day 32, Month 13 - both invalid)")
        reg_page.set_dob("32-13-2022") 
        time.sleep(3) # Wait to observe the invalid date
        
        self.logger.info("Attempting to submit with invalid DOB...")
        reg_page.click_continue()
        time.sleep(2)
        
        if "eligibility" in self.driver.current_url.lower():
             self.logger.error("FAILED: Invalid DOB accepted.")
             assert False
        else:
             self.logger.info("PASSED: Invalid DOB blocked submission.")
             time.sleep(2)
             
        # --- 6. Empty Gender ---
        self.logger.info(">>> Check 6: Empty Gender")
        self.driver.refresh()
        time.sleep(3)
        reg_page.handle_modal()
        
        # Fill all mandatory EXCEPT Gender
        reg_page.set_name("Valid Name")
        reg_page.set_father_name("Father Valid")
        reg_page.set_mother_name("Mother Valid")
        reg_page.set_dob("01-01-1990")
        reg_page.set_udise_code("10101000101")
        reg_page.click_verify_udise()
        reg_page.handle_modal()
        
        # Ensure Gender is NOT selected (implicit from refresh)
        
        reg_page.click_continue()
        time.sleep(2)
        
        if "eligibility" in self.driver.current_url.lower():
             self.logger.error("FAILED: Empty Gender accepted.")
             assert False
        else:
             self.logger.info("PASSED: Empty Gender blocked submission.")
             time.sleep(2)

    def test_registration_step3_invalid_email_mobile(self, setup):
        """
        Scenario: 
        1. Fill Step 1 & 2 validly.
        2. At Step 3 (Authentication), enter invalid email format.
        3. Enter invalid mobile format.
        Expected: Validation errors.
        """
        self.logger.info("**** Starting Negative Test: Step 3 Invalid Data ****")
        self.driver = setup
        self.driver.get(self.baseURL)
        
        # Pre-requisite: Reach Step 3
        self.fill_step1_basic_details(self.driver)
        self.fill_step2_eligibility(self.driver)
        
        auth_page = AuthenticationPage(self.driver)
        
        # 1. Invalid Email
        self.logger.info("Testing Invalid Email...")
        auth_page.set_email("invalid-email-format")
        auth_page.set_mobile("9876543210") # Valid mobile
        auth_page.click_submit()
        
        time.sleep(2)
        if "otp" in self.driver.current_url:
            self.logger.error("Negative Test FAILED: Accepted invalid email!")
            assert False
        else:
            self.logger.info("Negative Test PASSED: Blocked invalid email.")
            
        # Refresh or reset fields
        self.driver.refresh()
        time.sleep(2)
        
        # 2. Invalid Mobile
        self.logger.info("Testing Invalid Mobile...")
        auth_page.set_email("valid.email@example.com") # Valid email
        auth_page.set_mobile("123") # Invalid mobile
        auth_page.click_submit()
        
        time.sleep(2)
        if "otp" in self.driver.current_url:
            self.logger.error("Negative Test FAILED: Accepted invalid mobile!")
            assert False
        else:
            self.logger.info("Negative Test PASSED: Blocked invalid mobile.")
            
