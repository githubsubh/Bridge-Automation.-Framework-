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
        
        # 1. First Login Phase
        home_page = HomePage(self.driver)
        home_page.navigate_to_teacher_login()
        
        login_page = LoginPage(self.driver)
        if not login_page.login_with_manual_captcha(self.email, self.password, timeout=120):
            pytest.fail("First login failed.")
            
        
        self.logger.info("Login successful. Proceeding to features...")
        time.sleep(5)
        
        # 4. Feature Navigation: My Documents
        dashboard_page = DashboardPage(self.driver)
        self.logger.info("--- Feature 1: My Documents ---")
        time.sleep(5)
        assert dashboard_page.verify_my_documents(), "My Documents section missing"
        
        self.logger.info("Hovering 'View Documents'...")
        dashboard_page.mouse_hover(dashboard_page.link_view_documents)
        time.sleep(5)
        self.logger.info("Clicking 'View Documents'...")
        dashboard_page.do_click(dashboard_page.link_view_documents)
        
        time.sleep(5)
        self.logger.info("Returning to Dashboard...")
        self.driver.back()
        time.sleep(5)
        
        # 5. Feature Navigation: Print Application
        self.logger.info("--- Feature 2: Print Application ---")
        time.sleep(5)
        assert dashboard_page.verify_print_section(), "Print section missing"
        
        self.logger.info("Hovering 'Application Form'...")
        dashboard_page.mouse_hover(dashboard_page.link_print_application)
        time.sleep(5)
        self.logger.info("Clicking 'Application Form'...")
        dashboard_page.do_click(dashboard_page.link_print_application)
        
        time.sleep(5)
        self.logger.info("Handling Print View Tab...")
        windows = self.driver.window_handles
        if len(windows) > 1:
            self.driver.switch_to.window(windows[1])
            self.logger.info("Analyzing Print View...")
            time.sleep(5)
            self.driver.close()
            self.driver.switch_to.window(windows[0])
            
        self.logger.info("**** Sequential Functional Test Completed Successfully ****")
        time.sleep(5)
