import pytest
import time
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.documents_page import DocumentsPage
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen
from selenium.webdriver.common.by import By

class Test_010_DocumentsAndPrint:
    home_url = "https://bridge-uat.nios.ac.in/"
    email = ReadConfig.getLoginEmail()
    password = ReadConfig.getLoginPassword()
    logger = LogGen.loggen()
    
    def test_docs_and_print_flow(self, setup):
        self.logger.info("**** Starting Test_010_DocumentsAndPrint ****")
        self.driver = setup
        self.driver.get(self.home_url)
        
        # 1. Login
        home_page = HomePage(self.driver)
        home_page.navigate_to_teacher_login()
        
        login_page = LoginPage(self.driver)
        if not login_page.login_with_manual_captcha(self.email, self.password, timeout=120):
            pytest.fail("Login failed, cannot test Documents & Print.")
            
        self.logger.info("Login successful. Waiting 5 seconds on Dashboard...")
        time.sleep(5)
        
        dashboard_page = DashboardPage(self.driver)
        
        # 2. Phase 1: My Documents Verification
        self.logger.info("--- Phase 1: Verifying 'My Documents' ---")
        dashboard_page.mouse_hover(dashboard_page.link_view_documents)
        time.sleep(2)
        dashboard_page.do_click(dashboard_page.link_view_documents)
        
        docs_page = DocumentsPage(self.driver)
        self.logger.info("Waiting 5 seconds for Documents page to load...")
        time.sleep(5)
        
        if docs_page.verify_documents_displayed():
            self.logger.info("Documents page verified successfully.")
        else:
            self.logger.warning("Documents page verification failed or elements missing.")
            
        self.logger.info("Testing Sample Document link...")
        docs_page.click_sample_document()
        time.sleep(3) # Wait to show the action
        
        # Navigate back to Dashboard
        self.logger.info("Navigating back to Dashboard...")
        self.driver.get(self.home_url + "teacher/dashboard") # Direct URL for speed
        time.sleep(5)
        
        # 3. Phase 2: Print Application Flow (Tab Handling)
        self.logger.info("--- Phase 2: Verifying 'Print Application' ---")
        
        # Store current window handle
        main_window = self.driver.current_window_handle
        self.logger.info(f"Main Window Handle: {main_window}")
        
        dashboard_page.mouse_hover(dashboard_page.link_print_application)
        time.sleep(2)
        dashboard_page.do_click(dashboard_page.link_print_application)
        self.logger.info("Clicked Print Application. Waiting for new tab...")
        time.sleep(5)
        
        # Switch to the new tab
        all_handles = self.driver.window_handles
        for handle in all_handles:
            if handle != main_window:
                self.driver.switch_to.window(handle)
                self.logger.info(f"Switched to New Tab: {handle}")
                break
        
        # Verify Content in the New Tab
        try:
            self.logger.info("Verifying content in the print application tab...")
            # Look for common header text in the application form
            body_text = self.driver.find_element(By.TAG_NAME, "body").text
            if "Reference Number" in body_text or "Teacher Name" in body_text:
                self.logger.info("Application Form content detected in the new tab!")
            else:
                self.logger.warning("Could not clearly identify form content in the new tab body.")
            
            # Save a screenshot of the print view if possible (often it's a PDF or complex HTML)
            self.driver.save_screenshot("screenshots/print_view_tab.png")
            self.logger.info("Saved screenshot of the print view tab.")
            
        except Exception as e:
            self.logger.error(f"Error during print tab verification: {e}")
        
        # Close the tab and go back
        self.logger.info("Closing print tab and returning to main window...")
        self.driver.close()
        self.driver.switch_to.window(main_window)
        
        self.logger.info("**** Test_010_DocumentsAndPrint Completed Successfully ****")
        time.sleep(2)
