import pytest
import time
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.eservices_page import EServicesPage
from pages.payment_flow_page import PaymentFlowPage
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen
from utilities.data_utils import DataUtils
import random
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Test_006_EServices_Functional:
    home_url = "https://bridge-uat.nios.ac.in/"
    email = ReadConfig.getLoginEmail()
    password = ReadConfig.getLoginPassword()
    logger = LogGen.loggen()
    
    # List of services to test sequentially
    # Each service must complete payment before the next starts
    # List of all 14 core E-Services to test sequentially
    services_to_test = [
        # "Change Appointment Date", 
        "Change Correspondence Address", 
        # "Change Disability Category", 
        # "Change DOB", 
        # "Change Permanent Address", 
        # "Change School", 
        # "Change Social Category", 
        # "Change Study Medium", 
        # "Change Study Medium for Pedagogy of Language-I", 
        # "Change Study Medium for Pedagogy of Language-II",
        # "Father Name Correction",
        # "Gender Correction",
        # "Mother Name Correction",
        # "Name Correction"
    ]

    # Payment Config
    gateway = "SabPaisa"
    card_mode = "Cards" 
    card_number = "4000020000000000"
    card_holder = "Test Automation User" 
    card_expiry = "12/30"
    card_cvv = "234"

    def test_apply_multiple_eservices(self, setup):
        self.logger.info("**** Starting Multi-Service E-Services Flow ****")
        self.driver = setup
        
        for service_name in self.services_to_test:
            self.logger.info(f"--- Starting Application for: {service_name} ---")
            # 1. Login Logic
            if "dashboard" not in self.driver.current_url.lower():
                self.logger.info("Not on dashboard. Navigating via Home Page...")
                self.driver.get(self.home_url)
                time.sleep(5)
                
                home_page = HomePage(self.driver)
                home_page.navigate_to_teacher_login()
                time.sleep(3)
                
                # Check if we were auto-logged in or reached dashboard
                if "dashboard" not in self.driver.current_url.lower():
                    login_page = LoginPage(self.driver)
                    self.logger.info("On Login Page. Please enter CAPTCHA.")
                    if not login_page.login_with_manual_captcha(self.email, self.password, timeout=300):
                        pytest.fail(f"Login failed for service {service_name}")
                    self.logger.info("Login successful.")
                    time.sleep(5)
                else:
                    self.logger.info("Redirected to dashboard automatically.")
            else:
                self.logger.info("Already on dashboard.")
            
            dashboard_page = DashboardPage(self.driver)
            eservices_page = EServicesPage(self.driver)
            payment_page = PaymentFlowPage(self.driver)

            # 2. Navigate to Apply
            self.logger.info(f"Navigating to Apply page for {service_name}...")
            if dashboard_page.is_visible(dashboard_page.link_eservices_apply):
                dashboard_page.do_click(dashboard_page.link_eservices_apply)
                time.sleep(5)
            else:
                self.logger.error("Apply link not visible.")
                continue

            # 3. Click Specific Service
            if eservices_page.click_service_by_name(service_name):
                 self.logger.info(f"Service '{service_name}' selected.")
                 time.sleep(5)
            else:
                 self.logger.error(f"Service '{service_name}' not found.")
                 continue

            # 4. Initial Form / OTP Verification Phase
            self.logger.info("Handling Initial Form / OTP...")
            # Toggle any checkboxes if any
            try:
                 for cb in self.driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']"):
                     if not cb.is_selected(): self.driver.execute_script("arguments[0].click();", cb)
            except: pass
            
            # Click generic Proceed
            xpath_proceed = "//button[contains(text(), 'Proceed') or contains(text(), 'Generate') or contains(text(), 'Submit') or contains(text(), 'CONTINUE')]"
            try:
                btn = self.driver.find_element(By.XPATH, xpath_proceed)
                self.driver.execute_script("arguments[0].click();", btn)
            except: pass
            
            self.logger.info("Waiting for Step 2 (Fill Form) or Step 3 (Payment)...")
            print(f"\nACTION: Verify OTP for {service_name} in browser if requested.\n")
            
            try:
                # Wait for user to complete OTP and reach next step
                WebDriverWait(self.driver, 300).until(
                    lambda d: any(x in d.current_url.lower() for x in ["fill-form", "payment", "review", "transaction"])
                )
            except:
                self.logger.error(f"Timed out at OTP/Form transition for {service_name}")
                continue

            time.sleep(5)

            # 5. Fill Form Phase (Step 2)
            # Use both URL check and element check for robustness
            is_fill_form = "fill-form" in self.driver.current_url.lower() or len(self.driver.find_elements(By.ID, "EserviceForm")) > 0
            
            if is_fill_form:
                self.logger.info(f"Filling Details for {service_name}...")
                
                # Save Full DOM for analysis
                try:
                    with open(f"eservices_{service_name.replace(' ', '_')}_dom.html", "w", encoding="utf-8") as f:
                        f.write(self.driver.page_source)
                except: pass

                # Advanced Form Filling
                time.sleep(5)
                try:
                    # 1. State & District handling (Specific for Address Change)
                    state_dd = self.driver.find_elements(By.ID, "state-dropdown-1")
                    if state_dd:
                        self.driver.execute_script("""
                            var select = arguments[0];
                            for (var i=0; i<select.options.length; i++) {
                                if (select.options[i].text.toUpperCase().indexOf("DELHI") !== -1) {
                                    select.selectedIndex = i; break;
                                }
                            }
                            select.dispatchEvent(new Event('change', { bubbles: true }));
                            if (window.jQuery) { $(select).trigger("chosen:updated"); }
                        """, state_dd[0])
                        time.sleep(4) # Wait for District AJAX

                    dist_dd = self.driver.find_elements(By.ID, "district-dropdown-1")
                    if dist_dd:
                        self.driver.execute_script("""
                            var select = arguments[0];
                            for (var i=0; i<select.options.length; i++) {
                                if (select.options[i].text.toUpperCase().indexOf("CENTRAL") !== -1) {
                                    select.selectedIndex = i; break;
                                }
                            }
                            select.dispatchEvent(new Event('change', { bubbles: true }));
                            if (window.jQuery) { $(select).trigger("chosen:updated"); }
                        """, dist_dd[0])

                    # 2. General Dropdowns (including Disability)
                    all_dd = self.driver.find_elements(By.TAG_NAME, "select")
                    for dd in all_dd:
                        try:
                            self.driver.execute_script("""
                                var select = arguments[0];
                                var isDisability = select.id.toLowerCase().indexOf("disability") !== -1 || select.name.toLowerCase().indexOf("disability") !== -1;
                                if ((select.selectedIndex <= 0 || isDisability) && select.options.length > 1) {
                                    for (var i=0; i<select.options.length; i++) {
                                        if (select.options[i].value !== "" && select.options[i].text.indexOf("Select") === -1) {
                                            select.selectedIndex = i; break;
                                        }
                                    }
                                    select.dispatchEvent(new Event('change', { bubbles: true }));
                                    if (window.jQuery) { $(select).trigger("chosen:updated"); }
                                }
                            """, dd)
                        except: pass

                    # 3. Handle 'REQUIRED DOCUMENTS' button to reveal upload fields
                    try:
                        req_docs_btn = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'REQUIRED DOCUMENTS')]")
                        if req_docs_btn and req_docs_btn[0].is_displayed():
                            self.driver.execute_script("arguments[0].click();", req_docs_btn[0])
                            time.sleep(2)
                    except: pass

                    # 4. Dates
                    date_inputs = self.driver.find_elements(By.XPATH, "//input[@type='date' or contains(@placeholder, 'Select') or contains(@class, 'datapick')]")
                    for di in date_inputs:
                        if di.is_displayed() and di.get_attribute("readonly") == None:
                            is_dob = "dob" in di.get_attribute("id").lower() or "birth" in di.get_attribute("id").lower()
                            if is_dob: new_date_str = "01-01-1996"
                            else:
                                start_dt = datetime(2018, 6, 28); end_dt = datetime(2023, 8, 11)
                                delta = end_dt - start_dt
                                new_date_str = (start_dt + timedelta(days=random.randrange(delta.days + 1))).strftime("%d-%m-%Y")
                            self.driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", di, new_date_str)

                    # 5. Text & Numeric Inputs
                    inputs = self.driver.find_elements(By.XPATH, "//input[@type='text' or @type='number' or @type='tel' or @type='email']")
                    for ti in inputs:
                        if ti.is_displayed() and ti.get_attribute("readonly") == None:
                            name_low = (ti.get_attribute("id") or ti.get_attribute("name") or "").lower()
                            val = ""
                            if any(x in name_low for x in ["address1", "house", "building"]): val = "101 ddnagar"
                            elif any(x in name_low for x in ["address2", "street", "locality"]): val = "DD NAGAR"
                            elif "pincode" in name_low or "zip" in name_low: val = "110034"
                            elif not ti.get_attribute("value"): val = "UPDATED TEST DATA"
                            
                            if val:
                                self.driver.execute_script("arguments[0].value = '';", ti)
                                ti.send_keys(val)
                                self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true })); arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", ti)

                    # 6. File Uploads
                    file_inputs = self.driver.find_elements(By.XPATH, "//input[@type='file']")
                    if file_inputs:
                        _, doc_path = DataUtils.ensure_dummy_files()
                        for fi in file_inputs:
                            try: fi.send_keys(doc_path); self.logger.info("Uploaded document.")
                            except: pass
                except Exception as e:
                    self.logger.warning(f"Form-filling error: {e}")

                time.sleep(3)
                # 7. Submit Form
                try:
                    submit_xpath = "//button[contains(text(), 'Submit') or contains(text(), 'Pay') or contains(text(), 'Next') or contains(text(), 'CONTINUE')]"
                    submit_btn = self.driver.find_element(By.XPATH, submit_xpath)
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'}); arguments[0].click();", submit_btn)
                    self.logger.info("Proceeded from Fill Form Step.")
                except Exception as e:
                    self.logger.error(f"Submit click failed: {e}")
                    try: self.driver.execute_script("document.querySelector('button.btn-primary').click();")
                    except: pass

                time.sleep(5)
                # Wait for Payment/Review
                try:
                    WebDriverWait(self.driver, 60).until(
                        lambda d: any(x in d.current_url.lower() for x in ["payment", "review", "transaction", "otp", "request"])
                    )
                except:
                    self.logger.error(f"Timed out waiting for Payment page for {service_name}")
                    continue

            # 6. Payment Phase
            try:
                self.logger.info(f"Processing Payment Phase for {service_name}...")
                
                # Check for review page
                if "review" in self.driver.current_url.lower():
                    self.logger.info("On Review page, checking all confirmation boxes...")
                    payment_page.check_all_confirmation_boxes()
                    time.sleep(2)
                
                # Select Gateway
                payment_page.select_sabpaisa_gateway()
                payment_page.click_pay_now()
                
                time.sleep(5) # Reduced from 10s
                
                # Simulated Gateway Interaction
                if "sabpaisa" in self.driver.current_url.lower() or len(self.driver.find_elements(By.XPATH, "//*[contains(text(), 'SabPaisa')]")) > 0:
                    payment_page.select_payment_mode(self.card_mode)
                    time.sleep(3)
                    payment_page.enter_card_details(self.card_number, self.card_holder, self.card_expiry, self.card_cvv)
                    time.sleep(3)
                    payment_page.simulate_success()
                    self.logger.info(f"Payment interaction completed for {service_name}")
                else:
                    self.logger.warning(f"Gateway not detected for {service_name}. Moving to next service.")
            except Exception as e:
                self.logger.warning(f"Payment phase encountered an issue for {service_name}: {e}. Proceeding to dashboard.")

            # 7. Post-Payment / Cleanup
            time.sleep(3)
            self.logger.info(f"Moving back to Dashboard after {service_name}")
            self.driver.get(self.home_url + "teacher/dashboard")
            time.sleep(3)

        self.logger.info("**** Multi-Service Test Completed ****")
        time.sleep(5)

