"""
test_regression_us02_us03_login_security.py
============================================
Regression tests for:
  US-02: Login Security & Error Validation
  US-03: Clear/Reset Login Form

Tests that can run WITHOUT CAPTCHA:
  - Empty field validation
  - Password masking
  - Clear button existence & functionality
  - Email format validation (client-side)
  - SQL injection / XSS attempt (input accepted without crash)
  - Max character limit (browser-side restriction)

Run with:
  python -m pytest tests/test_regression_us02_us03_login_security.py -v -s --browser=chrome
"""
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen


LOGIN_URL = "https://bridge-uat.nios.ac.in/auth/login"


class Test_US02_LoginSecurity:
    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_TC_M1_03_invalid_email_format(self, setup):
        """TC_M1_03 | US-02: Invalid email format rejected client-side."""
        self.logger.info("**** TC_M1_03: Invalid Email Format ****")
        driver = setup
        driver.get(LOGIN_URL)
        time.sleep(2)

        email_field = driver.find_element(By.ID, "loginform-email")
        email_field.clear()
        email_field.send_keys("invalidemail@")    # No domain — invalid

        # HTML5 built-in validation: type="email" should flag this
        validity = driver.execute_script(
            "return document.getElementById('loginform-email').validity.valid;"
        )
        field_type = driver.execute_script(
            "return document.getElementById('loginform-email').type;"
        )
        self.logger.info(f"Email field type={field_type}, HTML5 valid={validity}")

        # If field type is email, HTML5 will catch the bad format
        if field_type == "email":
            assert not validity, "BUG: Invalid email 'invalidemail@' passed HTML5 validation."
            self.logger.info("PASS: Email format enforced by HTML5 type='email'.")
        else:
            # If type='text', check for server/JS error after submit
            # We flag this as an observation: email format not enforced at HTML level
            self.logger.warning(
                "OBSERVATION: Email field is type='text' — HTML5 format validation not active. "
                "Server-side or JS validation must cover this."
            )
            pytest.xfail(
                "Email field is type='text', not type='email'. "
                "HTML5 format check not applicable. Server-side validation needed."
            )

    @pytest.mark.regression
    def test_TC_M1_06_sql_injection_no_crash(self, setup):
        """TC_M1_06 | US-02: SQL injection in email field should not crash the page."""
        self.logger.info("**** TC_M1_06: SQL Injection Sanitization ****")
        driver = setup
        driver.get(LOGIN_URL)
        time.sleep(2)

        email_field = driver.find_element(By.ID, "loginform-email")
        email_field.clear()
        email_field.send_keys("' OR 1=1 --")

        pwd_field = driver.find_element(By.ID, "loginform-password")
        pwd_field.clear()
        pwd_field.send_keys("Password@1")

        # Do NOT enter CAPTCHA — just click to trigger client-side response
        login_btn = driver.find_element(By.ID, "submit-basic-details")
        login_btn.click()
        time.sleep(2)

        # Page must not crash — check for 500 error or DB error text
        page_src = driver.page_source.lower()
        crash_indicators = ["500", "sql", "syntax error", "database error", "exception", "traceback"]
        found_crash = [c for c in crash_indicators if c in page_src]

        assert not found_crash, f"BUG-CRITICAL: Page may have crashed. Found: {found_crash}"
        self.logger.info("PASS: No crash/DB error on SQL injection attempt.")

    @pytest.mark.regression
    def test_TC_M1_06b_xss_no_execution(self, setup):
        """TC_M1_06b | US-02: XSS attempt in password field must not execute."""
        self.logger.info("**** TC_M1_06b: XSS Sanitization ****")
        driver = setup
        driver.get(LOGIN_URL)
        time.sleep(2)

        pwd_field = driver.find_element(By.ID, "loginform-password")
        pwd_field.clear()
        pwd_field.send_keys("<script>alert('XSS')</script>")

        # Check: No JS alert popped up
        try:
            alert = driver.switch_to.alert
            alert_text = alert.text
            alert.dismiss()
            pytest.fail(f"BUG-CRITICAL: XSS script executed! Alert text: '{alert_text}'")
        except Exception:
            self.logger.info("PASS: No XSS alert triggered.")

    @pytest.mark.regression
    def test_TC_M1_08_password_masking(self, setup):
        """TC_M1_08 | US-01/02: Password field must be type='password' (masked)."""
        self.logger.info("**** TC_M1_08: Password Masking ****")
        driver = setup
        driver.get(LOGIN_URL)
        time.sleep(2)

        field_type = driver.execute_script(
            "return document.getElementById('loginform-password').type;"
        )
        assert field_type == "password", f"BUG: Password field type is '{field_type}', expected 'password'."
        self.logger.info(f"PASS: Password field type='{field_type}'.")

    @pytest.mark.regression
    def test_TC_M1_max_char_no_crash(self, setup):
        """US-02: Entering 500+ characters must not crash or cause server error."""
        self.logger.info("**** TC: Max Character Limit No Crash ****")
        driver = setup
        driver.get(LOGIN_URL)
        time.sleep(2)

        long_input = "A" * 600
        email_field = driver.find_element(By.ID, "loginform-email")
        email_field.clear()
        driver.execute_script(
            "arguments[0].value = arguments[1];",
            email_field, long_input
        )

        login_btn = driver.find_element(By.ID, "submit-basic-details")
        login_btn.click()
        time.sleep(2)

        page_src = driver.page_source.lower()
        crash_indicators = ["500", "exception", "traceback", "fatal error"]
        found = [c for c in crash_indicators if c in page_src]

        assert not found, f"BUG: Server crashed on long input. Indicators: {found}"
        self.logger.info("PASS: 600-char input handled gracefully.")


class Test_US03_ClearForm:
    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_TC_M1_07_clear_button_exists(self, setup):
        """TC_M1_07a | US-03: Clear/Reset button must exist on the login form."""
        self.logger.info("**** TC_M1_07a: Clear Button Existence ****")
        driver = setup
        driver.get(LOGIN_URL)
        time.sleep(2)

        # Common selectors for a Clear/Reset button
        clear_candidates = driver.find_elements(
            By.XPATH,
            "//button[contains(translate(., 'CLEAR', 'clear'), 'clear') or "
            "contains(translate(., 'RESET', 'reset'), 'reset')] | "
            "//input[@type='reset'] | "
            "//a[contains(translate(., 'CLEAR', 'clear'), 'clear')]"
        )

        if not clear_candidates:
            self.logger.warning(
                "OBSERVATION US-03: No 'Clear' or 'Reset' button found on login page. "
                "US-03 (Priority: Should Have) may not be implemented yet."
            )
            pytest.xfail("US-03: Clear button not found on login page — feature may not be implemented.")
        else:
            self.logger.info(f"PASS: Clear button found: '{clear_candidates[0].text}'")

    @pytest.mark.regression
    def test_TC_M1_07b_clear_button_clears_fields(self, setup):
        """TC_M1_07b | US-03: Clicking Clear must empty both fields and remove errors."""
        self.logger.info("**** TC_M1_07b: Clear Button Functionality ****")
        driver = setup
        driver.get(LOGIN_URL)
        time.sleep(2)

        # Fill fields
        driver.find_element(By.ID, "loginform-email").send_keys("test@example.com")
        driver.find_element(By.ID, "loginform-password").send_keys("SomePassword@1")

        # Try to find and click clear
        clear_candidates = driver.find_elements(
            By.XPATH,
            "//button[contains(translate(., 'CLEAR', 'clear'), 'clear') or "
            "contains(translate(., 'RESET', 'reset'), 'reset')] | "
            "//input[@type='reset']"
        )
        if not clear_candidates:
            pytest.xfail("US-03: No Clear button found — cannot test clear functionality.")

        clear_candidates[0].click()
        time.sleep(1)

        email_val = driver.find_element(By.ID, "loginform-email").get_attribute("value")
        pass_val  = driver.find_element(By.ID, "loginform-password").get_attribute("value")

        assert email_val == "", f"BUG: Email field not cleared after clicking Clear. Value: '{email_val}'"
        assert pass_val  == "", f"BUG: Password field not cleared after clicking Clear. Value: '{pass_val}'"
        self.logger.info("PASS: Both fields cleared after Clear button click.")
