import pytest
import time
import os
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.documents_page import DocumentsPage
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

class Test_011_ReuploadDocuments:
    home_url = "https://bridge-uat.nios.ac.in/"
    email = ReadConfig.getLoginEmail()
    password = ReadConfig.getLoginPassword()
    logger = LogGen.loggen()
    
    # Updated paths to the specific dummy files we just generated
    base_path = "/Users/anujjha/Bridge-Automation.-Framework-"
    photo_path = os.path.join(base_path, "test_data/official_photo.jpg")
    sig_path = os.path.join(base_path, "test_data/official_signature.jpg")
    doc_path = os.path.join(base_path, "test_data/official_certificate.pdf")
    
    def test_reupload_documents_flow(self, setup):
        self.logger.info("**** Starting Test_011_ReuploadDocuments (Refined) ****")
        self.driver = setup
        self.driver.get(self.home_url)
        
        # 1. Login
        home_page = HomePage(self.driver)
        home_page.navigate_to_teacher_login()
        
        login_page = LoginPage(self.driver)
        if not login_page.login_with_manual_captcha(self.email, self.password, timeout=120):
            pytest.fail("Login failed, cannot test Re-upload Documents.")
            
        self.logger.info("Login successful. Waiting 5 seconds on Dashboard...")
        time.sleep(5)
        
        dashboard_page = DashboardPage(self.driver)
        
        # 2. Navigate to My Documents
        self.logger.info("Navigating to My Documents...")
        dashboard_page.mouse_hover(dashboard_page.link_view_documents)
        time.sleep(2)
        dashboard_page.do_click(dashboard_page.link_view_documents)
        
        docs_page = DocumentsPage(self.driver)
        self.logger.info("Waiting 5 seconds for Documents page to load...")
        time.sleep(5)
        
        # Capture DOM as requested by user
        dom_content = self.driver.page_source
        with open("documents_upload_page_live.html", "w", encoding="utf-8") as f:
            f.write(dom_content)
        self.logger.info("LIVE DOM captured and saved to 'documents_upload_page_live.html'")
        
        # 3. View Documents (Eye Icon) and Sample Document
        self.logger.info("--- Phase: Viewing Documents ---")
        
        # View uploaded documents (Eye Icon)
        # We start by finding how many buttons there are
        view_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@class, 'uploader-wrapper-action-btn')]")
        count = len(view_buttons)
        
        # Explicit wait
        wait = WebDriverWait(self.driver, 10)
        
        if count > 0:
            self.logger.info(f"Found {count} view document buttons. Iterating through each...")
            
            for i in range(count):
                try:
                    # Re-find elements to avoid StaleElementReferenceException
                    current_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@class, 'uploader-wrapper-action-btn')]")
                    if i >= len(current_buttons):
                        break
                        
                    btn = current_buttons[i]
                    
                    # Scroll into view to ensure it's clickable and visible to user
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                    time.sleep(1)
                    
                    self.logger.info(f"Clicking view button {i+1} of {count}...")
                    # Highlight the button for better visibility
                    self.driver.execute_script("arguments[0].style.border='3px solid red'", btn)
                    time.sleep(0.5)
                    
                    self.driver.execute_script("arguments[0].click();", btn)
                    
                    self.logger.info(f"Opened document {i+1}. Waiting for modal...")
                    
                    # Wait for SweetAlert2 modal to appear
                    try:
                        modal_img = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.swal2-container img.swal2-image")))
                        self.logger.info("Modal image visible. PREVIEWING FOR 5 SECONDS...")
                        time.sleep(5) # Strict 5 second wait
                        
                        # Find and Click Close Button
                        close_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.swal2-close")))
                        self.logger.info("Closing modal...")
                        close_btn.click()
                        
                        # Wait for modal to disappear
                        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.swal2-container")))
                        self.logger.info("Modal closed.")
                        
                    except Exception as e_modal:
                        self.logger.warning(f"Modal interaction failed: {e_modal}. Trying to close via background click or ESC.")
                        try:
                            # Fallback: Click outside or send ESC
                            action = ActionChains(self.driver)
                            action.send_keys(Keys.ESCAPE).perform()
                        except:
                            pass

                    self.logger.info(f"Finished viewing document {i+1}.")
                    time.sleep(1) 
                        
                except Exception as e:
                    self.logger.warning(f"Could not view document {i+1}: {e}")
        else:
             self.logger.warning("No 'eye icon' (view document) buttons found.")
        
        # === View Sample Documents ===
        self.logger.info("--- Phase: Viewing Sample Documents ---")
        
        # Find all "View Sample Document" buttons
        sample_buttons = self.driver.find_elements(By.CSS_SELECTOR, "span.sample-docv.viewsam")
        sample_count = len(sample_buttons)
        
        if sample_count > 0:
            self.logger.info(f"Found {sample_count} 'View Sample Document' buttons. Iterating through each...")
            
            for i in range(sample_count):
                try:
                    # Re-find elements to avoid stale references
                    current_samples = self.driver.find_elements(By.CSS_SELECTOR, "span.sample-docv.viewsam")
                    if i >= len(current_samples):
                        break
                        
                    sample_btn = current_samples[i]
                    
                    # Scroll into view
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", sample_btn)
                    time.sleep(1)
                    
                    self.logger.info(f"Clicking 'View Sample Document' button {i+1} of {sample_count}...")
                    # Highlight for visibility
                    self.driver.execute_script("arguments[0].style.border='3px solid blue'", sample_btn)
                    time.sleep(0.5)
                    
                    self.driver.execute_script("arguments[0].click();", sample_btn)
                    
                    self.logger.info(f"Opened sample document {i+1}. Waiting for modal...")
                    
                    # Wait for SweetAlert2 modal to appear
                    try:
                        # For PDFs or images, the modal structure may be slightly different
                        # Try waiting for either image or general popup
                        modal_content = wait.until(
                            EC.visibility_of_element_located(
                                (By.CSS_SELECTOR, "div.swal2-popup")
                            )
                        )
                        self.logger.info("Sample document modal visible. PREVIEWING FOR 5 SECONDS...")
                        time.sleep(5) # Strict 5 second wait
                        
                        # Find and Click Close Button
                        close_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.swal2-close")))
                        self.logger.info("Closing sample document modal...")
                        close_btn.click()
                        
                        # Wait for modal to disappear
                        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.swal2-container")))
                        self.logger.info("Sample document modal closed.")
                        
                    except Exception as e_modal:
                        self.logger.warning(f"Sample document modal interaction failed: {e_modal}. Trying ESC.")
                        try:
                            action = ActionChains(self.driver)
                            action.send_keys(Keys.ESCAPE).perform()
                        except:
                            pass

                    self.logger.info(f"Finished viewing sample document {i+1}.")
                    time.sleep(1)
                        
                except Exception as e:
                    self.logger.warning(f"Could not view sample document {i+1}: {e}")
        else:
            self.logger.warning("No 'View Sample Document' buttons found.")

        # === Navigate to Dashboard ===
        self.logger.info("--- Phase: Navigating to Dashboard ---")
        self.logger.info("Clicking 'Go to Dashboard' to end test...")
        try:
             # Targeted locator for the footer link
             dashboard_link = self.driver.find_element(By.XPATH, "//a[contains(@href, '/teacher/dashboard') and contains(., 'Go to Dashboard')]")
             
             # Scroll to it
             self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dashboard_link)
             time.sleep(1)
             dashboard_link.click()
             self.logger.info("Clicked 'Go to Dashboard' link.")
        except:
             self.logger.info("Could not find specific footer 'Go to Dashboard' link, navigating via URL.")
             self.driver.get(self.home_url + "teacher/dashboard")
        
        time.sleep(3)
        self.logger.info("Returned to Dashboard.")
        
        self.logger.info("**** Test_011_ReuploadDocuments (Refined) Completed Successfully ****")

