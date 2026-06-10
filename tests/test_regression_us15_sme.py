
import pytest
import time
from pages.sme_mgmt_page import SMEManagementPage
from pages.admin_login_page import AdminLoginPage
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen
from selenium.webdriver.common.by import By

class Test_US15_SME_Regression:
    admin_url = "https://bridge-uat.nios.ac.in/admin/login" # Inferred
    logger = LogGen.loggen()

    @pytest.mark.regression
    @pytest.mark.skip(reason="Requires Admin Login which has CAPTCHA")
    def test_TC_M6_01_sme_pan_validation(self, setup):
        """TC_M6_01: SME PAN Validation Regex enforcement [A-Z]{5}[0-9]{4}[A-Z]"""
        self.logger.info("**** Starting TC_M6_01: SME PAN Validation ****")
        driver = setup
        driver.get(self.admin_url)
        
        # Admin Login would be needed here...
        # For regression, we'll focus on the Add SME form if we can reach it.
        
        # This is a placeholder for the logic once we have a bypass or assisted login
        pass

    @pytest.mark.regression
    def test_US15_SME_Form_DOM_Check(self, setup):
        """Verify presence of key fields for SME Onboarding as per US-15."""
        self.logger.info("**** Checking SME Form DOM (if accessible) ****")
        driver = setup
        # If we can't login, we can't see the form. 
        # But we can check if the page exists or if we get redirected.
        driver.get("https://bridge-uat.nios.ac.in/expert/create") # Hypothetical URL
        
        # Check if we are on a login page or the actual form
        current_url = driver.current_url
        if "login" in current_url:
            self.logger.info("SME Form is protected by login. Skipping DOM check.")
            pytest.skip("SME Form is behind authentication.")
        else:
            # Check for fields
            sme_page = SMEManagementPage(driver)
            assert driver.find_element(*sme_page.NAME_FIELD)
            assert driver.find_element(*sme_page.AADHAAR_FIELD)
            self.logger.info("SME Form fields found in DOM.")
