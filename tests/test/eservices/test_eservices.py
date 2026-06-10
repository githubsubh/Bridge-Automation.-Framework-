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
    services_to_test = [
        "Change Disability Category"
    ]

    # Payment Config
    gateway = "SabPaisa"
    card_mode = "Cards" 
    card_number = "4029484589897107"
    card_holder = "Test Automation User" 
    card_expiry = "12/30"
    card_cvv = "234"

    def test_apply_multiple_eservices(self, setup):
        self.logger.info("**** Starting Multi-Service E-Services Flow ****")
        self.driver = setup
        
        # Initialize Pages
        home_page = HomePage(self.driver)
        login_page = LoginPage(self.driver)
        dashboard_page = DashboardPage(self.driver)
        eservices_page = EServicesPage(self.driver)
        payment_page = PaymentFlowPage(self.driver)

        # 1. Login Logic
        self.driver.get(self.home_url)
        if "dashboard" not in self.driver.current_url.lower():
            home_page.navigate_to_teacher_login()
            time.sleep(1)
            login_page.login_with_manual_captcha(self.email, self.password)
            time.sleep(2)  # Wait for login completion

        for service_name in self.services_to_test:
            self.logger.info(f"--- Starting Application for: {service_name} ---")
            
            # 2. Navigate to "Apply New Service"
            self.driver.get(self.home_url + "teacher/dashboard")
            try:
                # Wait for dashboard using implicit/explicit
                WebDriverWait(self.driver, 20).until(EC.url_contains("dashboard"))
            except:
                self.logger.warning("Dashboard load timeout. Continuing...")
            
            # Click "E-Services" -> "Apply New Service"
            # Assuming we are on dashboard
            try:
                # Use JS to click apply new service if needed, or normal click
                eservices_page.click_apply_new_service()
                time.sleep(2)
            except:
                self.logger.error("Could not click 'Apply New Service'. Checking if already on page.")

            # 3. Search & Select Service
            eservices_page.search_and_select_service(service_name)
            time.sleep(5)

            # 4. Handle "Form Filling"
            # We assume we are on the form page if URL contains 'fill-form' or form element exists
            is_fill_form = "fill-form" in self.driver.current_url.lower() or len(self.driver.find_elements(By.ID, "EserviceForm")) > 0
            
            if is_fill_form:
                self.logger.info(f"Filling Details for {service_name}...")
                time.sleep(2)
                
                # A. Handle Dropdowns (General & Special)
                all_dd = self.driver.find_elements(By.TAG_NAME, "select")
                for dd in all_dd:
                    try:
                        # Skip hidden/disabled/readonly
                        if not dd.is_displayed() or not dd.is_enabled() or dd.get_attribute("readonly"):
                            continue
                        
                        # Identify Special Dropdowns
                        dd_id_name = (dd.get_attribute("id") or "") + " " + (dd.get_attribute("name") or "")
                        dd_id_name = dd_id_name.lower()
                        is_special = any(x in dd_id_name for x in ["medium", "disability", "school"])
                        
                        # JS to select valid option (Special = Must Change Value)
                        self.driver.execute_script("""
                        var select = arguments[0];
                        var isSpecial = arguments[1];
                        if (select.disabled || select.hasAttribute("readonly")) return;
                        
                        var currentIndex = select.selectedIndex;
                        var pickedIndex = -1;
                        
                        if (isSpecial) {
                            // Find DIFFERENT value
                            for (var k=0; k<select.options.length; k++) {
                                var opt = select.options[k];
                                if (k !== currentIndex && opt.value !== "" && !opt.text.toLowerCase().includes("select")) {
                                    pickedIndex = k;
                                    break;
                                }
                            }
                            // Fallback if no different value found
                             if (pickedIndex === -1 && select.options.length > 1) {
                                 for (var k=0; k<select.options.length; k++) {
                                    if (select.options[k].value !== "") { pickedIndex=k; break; }
                                 }
                             }
                        } else {
                            // Find ANY valid value (if not already selected)
                            if (select.selectedIndex <= 0) {
                                for (var k=0; k<select.options.length; k++) {
                                    if (select.options[k].value !== "" && !select.options[k].text.toLowerCase().includes("select")) {
                                        pickedIndex = k;
                                        break;
                                    }
                                }
                            }
                        }
                        
                        if (pickedIndex !== -1) {
                            select.selectedIndex = pickedIndex;
                            select.dispatchEvent(new Event('change', { bubbles: true }));
                            if (window.jQuery) { $(select).trigger("chosen:updated"); $(select).change(); }
                        }
                        """, dd, is_special)
                        time.sleep(0.5)
                    except: pass

                # B. Handle Text Inputs
                inputs = self.driver.find_elements(By.TAG_NAME, "input")
                for inp in inputs:
                    try:
                        type_attr = inp.get_attribute("type")
                        if type_attr not in ["text", "number", "email", "tel"]: continue
                        if not inp.is_displayed() or not inp.is_enabled() or inp.get_attribute("readonly"): continue
                        
                        # Skip if Chosen.js search field
                        outer = inp.get_attribute("outerHTML")
                        if "chosen" in outer: continue
                        
                        # Randomized Date Handling
                        if "date" in (inp.get_attribute("id") or "").lower():
                            year = random.randint(1990, 2023)
                            month = random.randint(1, 12)
                            day = random.randint(1, 28)
                            val = f"{day:02d}-{month:02d}-{year}"
                            self.driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change'));", inp, val)
                            continue

                        # Text Entry
                        val = "Test Data"
                        # Simple JS set value
                        self.driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change'));", inp, val)
                    except: pass
                
                # C. Handle File Uploads (Generic)
                file_inputs = self.driver.find_elements(By.XPATH, "//input[@type='file']")
                if file_inputs:
                    _, doc_path = DataUtils.ensure_dummy_files()
                    for fi in file_inputs:
                        try: fi.send_keys(doc_path)
                        except: pass

                time.sleep(2)
                
                # 5. Submit Form
                try:
                    submit_xpath = "//button[contains(text(), 'Submit') or contains(text(), 'Pay') or contains(text(), 'Next') or contains(text(), 'CONTINUE')]"
                    submit_btn = self.driver.find_element(By.XPATH, submit_xpath)
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'}); arguments[0].click();", submit_btn)
                except Exception as e:
                    self.logger.error(f"Submit Failed: {e}")
                    # Try fallback
                    try: self.driver.execute_script("document.querySelector('button.btn-primary').click();")
                    except: pass
                
                time.sleep(5)

            # 6. Payment Phase
            try:
                self.logger.info(f"Processing Payment for {service_name}")
                if "review" in self.driver.current_url.lower():
                    self.logger.info("Handling Review Page...")
                    payment_page.check_all_confirmation_boxes()
                    time.sleep(1)
                
                payment_page.select_sabpaisa_gateway()
                payment_page.click_pay_now()
                time.sleep(5)
                
                # Nuclear Option for SabPaisa
                if "sabpaisa" in self.driver.current_url.lower() or len(self.driver.find_elements(By.XPATH, "//*[contains(text(), 'SabPaisa')]")) > 0:
                    self.logger.info("Executing Nuclear Payment Simulation...")
                    self.driver.execute_script("""
                        var radios = document.querySelectorAll("input[type='radio']");
                        for(var i=0; i<radios.length; i++) {
                            if(radios[i].value.toLowerCase().trim() === 'success') {
                                radios[i].click(); radios[i].checked = true;
                            }
                        }
                        var btn = document.getElementById("submit") || document.querySelector("button.btn-success");
                        if(btn) btn.click();
                    """)
                    time.sleep(5)

            except Exception as e:
                self.logger.warning(f"Payment logic failed: {e}")

            # 7. Return to Dashboard
            self.logger.info("Returning to Dashboard")
            self.driver.get(self.home_url + "teacher/dashboard")
            time.sleep(3)
        
        self.logger.info("**** Test Completed ****")
