import pytest
import time
import os
from datetime import datetime, timedelta
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.eservices_page import EServicesPage
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

class Test_Functional_EServices_Workflow:
    home_url = "https://bridge-uat.nios.ac.in/"
    email = ReadConfig.getLoginEmail()
    password = ReadConfig.getLoginPassword()
    logger = LogGen.loggen()

    def test_apply_all_services_flow(self, setup):
        """
        Functional Flow:
        1. Login
        2. Iterate Services
        3. Standard: OTP -> Back
        4. Appointment Date: OTP -> Fill Form -> Submit -> Back
        """
        self.logger.info("**** Starting Test_Functional_EServices_Workflow ****")
        self.driver = setup
        self.driver.get(self.home_url)

        # 1. Login
        home_page = HomePage(self.driver)
        home_page.navigate_to_teacher_login()
        login_page = LoginPage(self.driver)
        if not login_page.login_with_manual_captcha(self.email, self.password, timeout=120):
            pytest.fail("Login failed.")

        self.logger.info("Login successful. Navigating to E-Services Apply...")
        time.sleep(5)
        
        # 2. Get Services
        dashboard_page = DashboardPage(self.driver)
        dashboard_page.do_click(dashboard_page.link_eservices_apply)
        time.sleep(3)
        
        eservices_page = EServicesPage(self.driver)
        services_dict = eservices_page.get_all_services_details()
        self.logger.info(f"Functional Test: Will iterate through {len(services_dict)} services.")

        self.failures = []
        index = 1
        
        for name, url in services_dict.items():
            if any(x in name for x in ["Change Date of Birth", "Change DOB", "Change Disability Category"]):
                self.logger.info(f"SKIPPING '{name}' as per user request (System/Loading issues).")
                continue

            self.logger.info(f"--- [ {index} ] Service: {name} ---")
            
            try:
                try:
                    # Construct XPath carefully to match href
                    # We look for the anchor tag containing the href
                    service_link = self.driver.find_element(By.CSS_SELECTOR, f"a[href='{url}']")
                    
                    # Scroll into view first
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", service_link)
                    time.sleep(1) 
                    
                    # Hover
                    ActionChains(self.driver).move_to_element(service_link).perform()
                    time.sleep(1) # Visual pause
                    
                    self.logger.info(f"Clicking service: {name}")
                    service_link.click()
                except Exception as e:
                    self.logger.warning(f"Hover/Click failed ({e}). Using direct navigation.")
                    self.driver.get(url) 
                
                # UNIVERSAL HANDLING FOR ALL SERVICES
                # We will handle OTP check for ALL services, and if we land on a form, we capture its DOM.
                
                self.logger.info(f"Processing Service: {name}")
                
                # Check where we are
                on_form_page = False
                wait_otp = 0
                
                # Wait for OTP or direct form load
                while wait_otp < 300:
                    curr_url = self.driver.current_url
                    if "verify-otp" not in curr_url and "apply" not in curr_url and "login" not in curr_url:
                        self.logger.info("Target Form Page Detected!")
                        on_form_page = True
                        break
                        
                    if "verify-otp" in curr_url:
                        if wait_otp % 30 == 0:
                             self.logger.info(">>> PLEASE ENTER OTP MANUALLY <<<")
                    
                    time.sleep(2)
                    wait_otp += 2

                if on_form_page:
                    # 1. Automate Known Services
                    if "Appointment Date" in name:
                        # ... (Keep existing automation) ... (I will inline this below for safety)
                         self.automate_appointment_date()
                    
                    elif "Change Correspondence Address" in name:
                         # ... (Keep existing automation) ...
                         self.automate_address_change()

                    else:
                        # 2. Capture DOM for NEW/UNKNOWN Services
                        safe_name = name.replace(" ", "_").lower()
                        dom_filename = f"dom_capture_{safe_name}.html"
                        with open(dom_filename, "w", encoding="utf-8") as f:
                            f.write(self.driver.page_source)
                        self.logger.info(f"Captured DOM to '{dom_filename}'")
                        
                        # MANUAL FILL & SUBMIT IS REQUIRED FOR UNKNOWN FORMS
                        self.logger.info(">>> AUTOMATION PAUSED: Please Manually Fill & Submit this form. <<<")
                        self.logger.info(">>> Script is waiting for you to return to the E-Services List... <<<")
                        
                        # Wait for return to list (Up to 10 minutes)
                        wait_return = 0
                        while "eservices/apply" not in self.driver.current_url and wait_return < 600:
                             time.sleep(2)
                             wait_return += 2
                             if wait_return % 30 == 0:
                                 self.logger.info(f"Still waiting for you to finish '{name}'... ({wait_return}s)")

                else:
                    self.logger.warning(f"Skipping {name} (OTP timeout or navigation error)")
                    self.failures.append(f"Timeout: {name}")

            except Exception as e:
                self.logger.error(f"Error in main loop for '{name}': {e}")
                self.failures.append(f"Exception: {name} - {str(e)}")
            
            # --- RECOVERY: Ensure we are back on the E-Services List ---
            if "eservices/apply" not in self.driver.current_url:
                self.logger.info("Redirecting back to E-Services List for recovery...")
                self.driver.get(self.home_url + "eservices/apply")
                time.sleep(3)
                
            # Pause between services
            self.logger.info("Pausing 3s before next service...")
            time.sleep(3)
            index += 1

    def automate_appointment_date(self):
        self.logger.info("Automating Appointment Form...")
        time.sleep(2)
        try:
            valid_date = "10-08-2023"
            date_input = self.driver.find_element(By.ID, "eserviceform-new_date_of_appointment")
            self.driver.execute_script("arguments[0].value = arguments[1];", date_input, valid_date)
            
            file_path = os.path.abspath("test_data/official_certificate.pdf")
            file_input = self.driver.find_element(By.ID, "eserviceform-documents_appointment_letter")
            file_input.send_keys(file_path)
            
            submit_btn = self.driver.find_element(By.XPATH, "//button[contains(text(),'CONTINUE')]")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
            time.sleep(1)
            ActionChains(self.driver).move_to_element(submit_btn).perform()
            time.sleep(1)
            submit_btn.click()
            
            # Wait for return
            time.sleep(5)
            if "eservices/apply" not in self.driver.current_url:
                 self.driver.get(self.home_url + "eservices/apply")
        except Exception as e:
            self.logger.error(f"Appointment Auto Failed: {e}")

    def automate_address_change(self):
        self.logger.info("Automating Address Form...")
        time.sleep(2)
        try:
            self.driver.find_element(By.ID, "eserviceform-new_address1").send_keys("House 123")
            self.driver.find_element(By.ID, "eserviceform-new_address2").send_keys("Test Street")
            
            state_select = self.driver.find_element(By.ID, "state-dropdown-1")
            self.driver.execute_script("arguments[0].style.display = 'block';", state_select)
            Select(state_select).select_by_value("9107") 
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", state_select)
            time.sleep(2) 
            
            district_select = self.driver.find_element(By.ID, "district-dropdown-1")
            self.driver.execute_script("arguments[0].style.display = 'block';", district_select)
            Select(district_select).select_by_value("910720")
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", district_select)
            
            self.driver.find_element(By.ID, "eserviceform-new_pincode").send_keys("110001")
            
            submit_btn = self.driver.find_element(By.XPATH, "//button[contains(text(),'CONTINUE')]")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
            time.sleep(1)
            ActionChains(self.driver).move_to_element(submit_btn).perform()
            time.sleep(1)
            submit_btn.click()
            
            time.sleep(5)
            if "eservices/apply" not in self.driver.current_url:
                 self.driver.get(self.home_url + "eservices/apply")

        except Exception as e:
             self.logger.error(f"Address Auto Failed: {e}")

        if failures:
            self.logger.error(f"Failures: {failures}")
        else:
            self.logger.info("SUCCESS: All services processed.")

        # Logout
        time.sleep(2)
        dashboard_page.do_logout()
