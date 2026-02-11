import pytest
import time
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.eservices_page import EServicesPage
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Test_008_EServices_Negative:
    home_url = "https://bridge-uat.nios.ac.in/"
    email = ReadConfig.getLoginEmail()
    password = ReadConfig.getLoginPassword()
    logger = LogGen.loggen()
    
    def test_eservice_form_validation(self, setup):
        """
        Scenario: 
        1. Login
        2. Navigate to an E-Service (e.g., 'Change Appointment Date')
        3. Attempt to submit the form without filling mandatory fields.
        4. verify that validation errors appear and submission is blocked.
        """
        self.logger.info("**** Starting Negative E-Service Test: Form Validation ****")
        self.driver = setup
        self.driver.get(self.home_url)
        
        # --- 1. LOGIN ---
        home_page = HomePage(self.driver)
        home_page.navigate_to_teacher_login()
        
        login_page = LoginPage(self.driver)
        if not login_page.login_with_manual_captcha(self.email, self.password, timeout=120):
            pytest.fail("Login failed - Cannot proceed with negative testing.")
            
        time.sleep(5)
        dashboard_page = DashboardPage(self.driver)
        eservices_page = EServicesPage(self.driver)
        
        # --- 2. NAVIGATE TO SERVICE ---
        service_name = "Change Appointment Date"
        self.logger.info(f"Navigating to {service_name} for negative testing...")
        
        dashboard_page.do_click(dashboard_page.link_eservices_apply)
        time.sleep(3)
        
        if eservices_page.click_service_by_name(service_name):
             self.logger.info(f"Service '{service_name}' selected.")
        else:
             pytest.fail(f"Could not find service '{service_name}'")
             
        time.sleep(5)
        
        # --- 3. ATTEMPT SUBMIT EMPTY FORM ---
        # Depending on the service flow, we might need to click 'Proceed' first to get to the form.
        # Try generic proceed button to reach form
        try:
            xpath_proceed = "//button[contains(text(), 'Proceed') or contains(text(), 'Generate') or contains(text(), 'Submit')]"
            btn = self.driver.find_element(By.XPATH, xpath_proceed)
            btn.click()
            time.sleep(2)
        except:
            pass
            
        # Assert we are on a form page
        # Now try to find the "Final Submit" or "Next" button on the form page
        try:
            submit_xpath = "//button[contains(text(), 'Submit') or contains(text(), 'Pay') or contains(text(), 'Next')]"
            submit_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, submit_xpath)))
            
            # Scroll to it
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
            time.sleep(1)
            
            self.logger.info("Clicking Submit on empty form...")
            submit_btn.click()
            time.sleep(2)
            
            # --- 4. VERIFY VALIDATION ---
            # Look for HTML5 validation messages (browser default) or custom error messages
            # Custom errors often appear in spans with class 'text-danger' or similar
            error_msgs = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'error') or contains(@class, 'danger') or contains(@class, 'invalid')]")
            visible_errors = [e.text for e in error_msgs if e.is_displayed() and e.text.strip() != ""]
            
            if visible_errors:
                self.logger.info(f"Negative Test PASSED: Found validation errors: {visible_errors}")
                assert True
            else:
                # Check for browser built-in validation (required attribute)
                # If the URL is still the same and we haven't moved to payment, it's a pass.
                if "payment" not in self.driver.current_url.lower():
                     self.logger.info("Negative Test PASSED: Form submission blocked (URL did not change to payment).")
                     assert True
                else:
                     self.logger.error("Negative Test FAILED: Form submitted successfully with empty fields!")
                     assert False, "Form should not submit with empty mandatory fields."
                     
        except Exception as e:
            self.logger.error(f"Test Error: {e}")
            assert False
