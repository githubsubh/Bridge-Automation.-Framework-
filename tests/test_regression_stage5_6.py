import pytest
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.registration_page import RegistrationPage
from pages.authentication_page import AuthenticationPage
from pages.personal_information_page import PersonalInformationPage
from pages.address_details_page import AddressDetailsPage
from pages.subject_details_page import SubjectDetailsPage
from pages.documents_page import DocumentsPage
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen
from utilities.data_utils import DataUtils

class Test_US08_US09_Registration_Stage5_6:
    base_url = ReadConfig.getApplicationURL()
    logger = LogGen.loggen()

    def reach_subject_page(self, driver):
        """Helper to navigate to Stage 5 (Subject Details)"""
        driver.get(self.base_url)
        reg_page = RegistrationPage(driver)
        reg_page.handle_modal(timeout=3)
        reg_page.wait_for_form()
        
        # Stage 1: Basic
        reg_page.set_name(DataUtils.get_random_name())
        reg_page.set_father_name("Father Name")
        reg_page.set_mother_name("Mother Name")
        reg_page.set_dob("01-01-1990")
        reg_page.set_gender("Male")
        reg_page.set_udise_code("10101000101")
        try: reg_page.click_verify_udise()
        except: pass
        reg_page.click_continue()
        
        # Stage 2: Auth
        WebDriverWait(driver, 10).until(lambda d: "eligibility" in d.current_url or "authentication" in d.current_url)
        if "eligibility" in driver.current_url:
            try:
                driver.find_element(By.ID, "eligibility-date_of_appointment").send_keys("01-01-2022")
                driver.find_element(By.ID, "submit-eligibility").click()
            except: pass
        WebDriverWait(driver, 10).until(EC.url_contains("authentication"))
        auth_page = AuthenticationPage(driver)
        auth_page.set_email(DataUtils.generate_email_incremental())
        auth_page.set_mobile(DataUtils.get_fixed_mobile())
        auth_page.click_submit()
        
        # Stage 2: OTP (Auto-bypassed on UAT)
        try:
            WebDriverWait(driver, 20).until(
                lambda d: "personal" in d.current_url or "otp" in d.current_url
            )
            if "otp" in driver.current_url:
                self.logger.info("OTP page appeared — waiting for auto-redirect...")
                WebDriverWait(driver, 20).until(EC.url_contains("personal"))
            self.logger.info("Reached Personal Information page.")
        except Exception:
            self.logger.warning("Could not confirm personal page. Continuing anyway.")
        
        # Stage 3: Personal Info
        personal_page = PersonalInformationPage(driver)
        personal_page.set_social_category("General")
        personal_page.set_medium_of_study("English")
        personal_page.click_continue()
        
        # Stage 4: Address
        WebDriverWait(driver, 20).until(EC.url_contains("address"))
        address_page = AddressDetailsPage(driver)
        address_page.enter_address_line1("Address Line 1")
        address_page.select_state("DELHI")
        address_page.select_district("CENTRAL")
        address_page.enter_pincode("110034")
        address_page.click_continue()
        
        # Land on Stage 5
        WebDriverWait(driver, 20).until(EC.url_contains("subject"))
        self.logger.info("Reached Subject Details Page.")

    @pytest.mark.regression
    def test_tc_us08_01_mandatory_medium(self, setup):
        """TC_US08_01: Verify mandatory Medium selection on Subject page"""
        self.logger.info("**** Starting TC_US08_01: Subject Mandatory Medium ****")
        driver = setup
        self.reach_subject_page(driver)
        
        subject_page = SubjectDetailsPage(driver)
        # Click continue without selecting medium
        subject_page.click_continue()
        
        time.sleep(2)
        # Check for error
        body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        if "medium" not in body_text and "select" not in body_text:
             self.logger.warning("BUG: Subject medium validation NOT enforced.")
             pytest.fail("BUG: Mandatory medium validation missing on Subject Details page.")
        else:
             self.logger.info("Subject medium validation successful.")

    @pytest.mark.regression
    def test_tc_us09_02_invalid_file_format(self, setup):
        """TC_US09_02: Verify invalid file format validation on Document page"""
        self.logger.info("**** Starting TC_US09_02: Document Invalid Format ****")
        driver = setup
        self.reach_subject_page(driver)
        
        # Pass Stage 5
        subject_page = SubjectDetailsPage(driver)
        subject_page.select_any_medium_for_enabled_subjects()
        subject_page.click_continue()
        
        # Land on Stage 6
        WebDriverWait(driver, 20).until(EC.url_contains("document"))
        docs_page = DocumentsPage(driver)
        
        # Create dummy invalid file
        invalid_file = "test_script.exe"
        with open(invalid_file, "w") as f: f.write("Dummy")
        abs_path = os.path.abspath(invalid_file)
        
        try:
            # Upload to first available input
            file_input = driver.find_element(By.XPATH, "//input[@type='file']")
            file_input.send_keys(abs_path)
            time.sleep(1)
            
            # Click save
            docs_page.click_save_continue()
            time.sleep(2)
            
            body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
            if "format" not in body_text and "invalid" not in body_text:
                 self.logger.warning("BUG: Document file format validation NOT enforced.")
                 pytest.fail("BUG: File format validation (JPG/PDF only) is missing on Document page.")
            else:
                 self.logger.info("Document format validation successful.")
        finally:
            if os.path.exists(invalid_file): os.remove(invalid_file)
