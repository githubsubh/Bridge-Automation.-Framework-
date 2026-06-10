import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.registration_page import RegistrationPage
from pages.authentication_page import AuthenticationPage
from pages.personal_information_page import PersonalInformationPage
from pages.address_details_page import AddressDetailsPage
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen
from utilities.data_utils import DataUtils

class Test_US06_US07_Registration_Stage3_4:
    base_url = ReadConfig.getApplicationURL()
    logger = LogGen.loggen()

    def reach_personal_info_page(self, driver):
        """Helper to navigate through Stage 1, 2, and OTP to reach Stage 3 (Personal Information)"""
        driver.get(self.base_url)
        reg_page = RegistrationPage(driver)
        reg_page.handle_modal(timeout=3)
        reg_page.wait_for_form()
        
        # Step 1: Basic Details
        reg_page.set_name(DataUtils.get_random_name())
        reg_page.set_father_name("Father Name")
        reg_page.set_mother_name("Mother Name")
        reg_page.set_dob("01-01-1990")
        reg_page.set_gender("Male")
        reg_page.set_udise_code("10101000101")
        try: reg_page.click_verify_udise()
        except: pass
        reg_page.click_continue()
        
        # In this env, Eligibility or Authentication follows
        WebDriverWait(driver, 10).until(lambda d: "eligibility" in d.current_url or "authentication" in d.current_url)
        if "eligibility" in driver.current_url:
            try:
                driver.find_element(By.ID, "eligibility-date_of_appointment").send_keys("01-01-2022")
                driver.find_element(By.ID, "submit-eligibility").click()
            except: pass
            
        # Step 2: Authentication
        WebDriverWait(driver, 10).until(EC.url_contains("authentication"))
        auth_page = AuthenticationPage(driver)
        auth_page.set_email(DataUtils.generate_email_incremental())
        auth_page.set_mobile(DataUtils.get_fixed_mobile())
        auth_page.click_submit()
        
        # Step 3: OTP (Auto-bypassed on UAT)
        try:
            WebDriverWait(driver, 20).until(
                lambda d: "personal" in d.current_url or "otp" in d.current_url
            )
            if "otp" in driver.current_url:
                self.logger.info("OTP page appeared — waiting for auto-redirect...")
                WebDriverWait(driver, 20).until(EC.url_contains("personal"))
            self.logger.info("Reached Personal Information Page.")
        except Exception:
            self.logger.warning("Could not confirm personal page. Continuing anyway.")

    @pytest.mark.regression
    def test_tc_us06_01_mandatory_dropdowns(self, setup):
        """TC_US06_01: Verify mandatory field validation (Dropdowns) on Personal Info"""
        self.logger.info("**** Starting TC_US06_01: Personal Info Mandatory Dropdowns ****")
        driver = setup
        self.reach_personal_info_page(driver)
        
        personal_page = PersonalInformationPage(driver)
        # Click continue without selecting dropdowns
        personal_page.click_continue()
        
        time.sleep(2)
        error_elements = driver.find_elements(By.XPATH, "//*[contains(@class,'help-block') or contains(@class,'invalid-feedback')]")
        all_errors = " ".join([e.text for e in error_elements if e.text]).lower()
        
        if "required" not in all_errors and "blank" not in all_errors:
            self.logger.warning("BUG: Personal Info mandatory dropdown validation NOT enforced.")
            pytest.fail("BUG: Mandatory dropdown validation missing on Personal Information page.")
        else:
            self.logger.info("Personal Info dropdown validation successful.")

    @pytest.mark.regression
    def test_tc_us07_03_pincode_length(self, setup):
        """TC_US07_03: Verify Pincode length validation on Address Details"""
        self.logger.info("**** Starting TC_US07_03: Address Pincode Length Validation ****")
        driver = setup
        # For this test, we need to pass Personal Info first
        self.reach_personal_info_page(driver)
        personal_page = PersonalInformationPage(driver)
        personal_page.set_social_category("General")
        personal_page.set_medium_of_study("English")
        personal_page.click_continue()
        
        # Land on Address Details
        WebDriverWait(driver, 20).until(EC.url_contains("address"))
        address_page = AddressDetailsPage(driver)
        
        # Enter 5-digit pincode
        self.logger.info("Entering 5-digit Pincode: '11003'")
        address_page.enter_pincode("11003")
        address_page.click_continue()
        
        time.sleep(2)
        error_elements = driver.find_elements(By.XPATH, "//*[contains(@class,'help-block') or contains(@class,'invalid-feedback')]")
        all_errors = " ".join([e.text for e in error_elements if e.text]).lower()
        
        if "6" not in all_errors and "digit" not in all_errors:
            self.logger.warning("BUG: Address Pincode length validation NOT enforced.")
            pytest.fail("BUG: Pincode length validation is missing on Address page.")
        else:
            self.logger.info("Pincode validation successful.")
