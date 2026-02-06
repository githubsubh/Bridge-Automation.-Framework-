import pytest
import time
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen

class Test_007_DashboardNavigation:
    home_url = "https://bridge-uat.nios.ac.in/"
    email = ReadConfig.getLoginEmail()
    password = ReadConfig.getLoginPassword()
    logger = LogGen.loggen()
    
    def test_dashboard_links_navigation(self, setup):
        self.logger.info("**** Starting Test_007_DashboardNavigation ****")
        self.driver = setup
        self.driver.get(self.home_url)
        
        # 1. Login
        home_page = HomePage(self.driver)
        home_page.navigate_to_teacher_login()
        
        login_page = LoginPage(self.driver)
        if not login_page.login_with_manual_captcha(self.email, self.password, timeout=120):
            pytest.fail("Login failed, cannot test Dashboard Navigation.")
            
        self.logger.info("Login successful. Waiting 5 seconds on Dashboard...")
        time.sleep(5)
        
        dashboard_page = DashboardPage(self.driver)
        
        # 2. Verify "My Documents" section and navigate
        self.logger.info("--- Testing 'My Documents' ---")
        assert dashboard_page.verify_my_documents(), "My Documents section verification failed"
        
        self.logger.info("Moving mouse to 'View Documents' link...")
        dashboard_page.mouse_hover(dashboard_page.link_view_documents)
        time.sleep(2)
        dashboard_page.do_click(dashboard_page.link_view_documents)
        
        self.logger.info("Waiting 5 seconds on My Documents page...")
        time.sleep(5)
        
        # Save DOM for analysis
        with open("documents_view_dom.html", "w", encoding="utf-8") as f:
            f.write(self.driver.page_source)
        self.logger.info("Saved Documents page DOM.")
        
        # Navigate back
        self.driver.back()
        time.sleep(5)
        
        # 3. Verify "Print" section and navigate
        self.logger.info("--- Testing 'Print Application' ---")
        assert dashboard_page.verify_print_section(), "Print section verification failed"
        
        self.logger.info("Moving mouse to 'Application Form' link...")
        dashboard_page.mouse_hover(dashboard_page.link_print_application)
        time.sleep(2)
        dashboard_page.do_click(dashboard_page.link_print_application)
        
        self.logger.info("Waiting 5 seconds to show Application Form...")
        time.sleep(5)
        
        # Note: This link has target="_blank", so it might open in a new tab.
        windows = self.driver.window_handles
        if len(windows) > 1:
            self.driver.switch_to.window(windows[1])
            self.logger.info("Switched to Print View window.")
            time.sleep(3)
            # Save DOM of print view if possible (often just a large table)
            with open("print_view_dom.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            self.driver.close()
            self.driver.switch_to.window(windows[0])
            self.logger.info("Returned to main dashboard window.")
        else:
            self.logger.info("Application Form did not open in a new window.")
            
        self.logger.info("**** Test_007_DashboardNavigation Completed Successfully ****")
        time.sleep(2)
