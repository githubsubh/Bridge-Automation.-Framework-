import pytest
import time
from pages.login_page import LoginPage
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen
from selenium.webdriver.common.by import By

class Test_US01_Login:
    login_url = "https://bridge-uat.nios.ac.in/auth/login"
    valid_email = ReadConfig.getLoginEmail()
    valid_password = ReadConfig.getLoginPassword()
    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_tc_us01_02_empty_fields_validation(self, setup):
        """TC_US01_02: Verify login validation with empty fields"""
        self.logger.info("**** Starting TC_US01_02: Empty Fields Validation ****")
        driver = setup
        driver.get(self.login_url)
        
        login_page = LoginPage(driver)
        # Click login without entering anything
        login_page.click_login()
        time.sleep(2)
        
        # Check for inline error messages: "This field is required"
        errors = driver.find_elements(By.XPATH, "//*[contains(text(), 'required') or contains(text(), 'cannot be blank')]")
        
        assert len(errors) >= 2, f"Expected at least 2 inline error messages for empty fields, found {len(errors)}"
        self.logger.info("Empty fields validation successful.")

    @pytest.mark.regression
    def test_tc_us01_03_invalid_password(self, setup):
        """TC_US01_03: Verify login failure with invalid password"""
        self.logger.info("**** Starting TC_US01_03: Invalid Password Validation ****")
        driver = setup
        driver.get(self.login_url)
        
        login_page = LoginPage(driver)
        login_page.set_email("test_valid_format@example.com")
        login_page.set_password("WrongPassword123!")
        
        login_page.click_login()
        time.sleep(2)
        
        # Checking for the alert
        error_msg = login_page.get_login_error_message()
        assert any(word in error_msg.lower() for word in ["invalid", "incorrect", "password", "captcha"]), f"Unexpected error message: {error_msg}"
        self.logger.info("Invalid password validation successful.")

    @pytest.mark.regression
    def test_tc_us01_04_password_masking(self, setup):
        """TC_US01_04: Verify UI/UX password field masking"""
        self.logger.info("**** Starting TC_US01_04: Password Masking Check ****")
        driver = setup
        driver.get(self.login_url)
        
        login_page = LoginPage(driver)
        pass_field = driver.find_element(*login_page.textbox_password_id)
        
        field_type = pass_field.get_attribute("type")
        assert field_type == "password", f"Expected type='password', got '{field_type}'"
        self.logger.info("Password masking check successful.")

    @pytest.mark.regression
    def test_tc_us01_01_successful_login(self, setup):
        """TC_US01_01: Verify successful login with valid credentials"""
        self.logger.info("**** Starting TC_US01_01: Successful Login ****")
        driver = setup
        driver.get(self.login_url)
        
        login_page = LoginPage(driver)
        
        # Manual CAPTCHA wait for successful login
        success = login_page.login_with_manual_captcha(self.valid_email, self.valid_password, timeout=120)
        
        assert success, "Login failed or timed out."
        self.logger.info("Successful Login validation passed.")
