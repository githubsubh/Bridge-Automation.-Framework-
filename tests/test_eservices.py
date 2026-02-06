import pytest
import time
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.eservices_page import EServicesPage
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen

class Test_006_EServices:
    home_url = "https://bridge-uat.nios.ac.in/"
    email = ReadConfig.getLoginEmail()
    password = ReadConfig.getLoginPassword()
    logger = LogGen.loggen()
    
    def test_eservices_navigation(self, setup):
        self.logger.info("**** Starting Test_006_EServices ****")
        self.driver = setup
        self.driver.get(self.home_url)
        
        # 1. Login
        home_page = HomePage(self.driver)
        home_page.navigate_to_teacher_login()
        
        login_page = LoginPage(self.driver)
        if not login_page.login_with_manual_captcha(self.email, self.password, timeout=120):
            pytest.fail("Login failed, cannot test E-Services.")
            
        self.logger.info("Login successful. Waiting 5 seconds on Dashboard...")
        time.sleep(5)
        
        dashboard_page = DashboardPage(self.driver)
        eservices_page = EServicesPage(self.driver)
        
        # 2. Test "Apply for E-Services"
        self.logger.info("--- Clicking 'Apply for E-Services' ---")
        if dashboard_page.is_visible(dashboard_page.link_eservices_apply):
            self.logger.info("Moving mouse to E-Services -> Apply link...")
            dashboard_page.mouse_hover(dashboard_page.link_eservices_apply)
            time.sleep(2) # Show intent
            dashboard_page.do_click(dashboard_page.link_eservices_apply)
            
            self.logger.info("Clicked Apply. Waiting 5 seconds to show the services list...")
            time.sleep(5) 
            
            # Save DOM for service list analysis
            with open("eservices_apply_dom.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            self.logger.info("Saved E-Services Apply page DOM.")
            
            assert eservices_page.verify_apply_page(), "Apply E-Services page verification failed"
        else:
            pytest.fail("E-Services 'Apply' link not found.")
            
        # 2.1 Test clicking a specific service
        self.logger.info("--- Clicking a specific service: 'Change DOB' ---")
        eservices_page.click_service_by_name("Change DOB")
        time.sleep(5)
        
        # 3. Test "My Requests"
        self.logger.info("Returning to Dashboard for next navigation...")
        self.driver.get("https://bridge-uat.nios.ac.in/teacher/dashboard") 
        time.sleep(5) # Wait on dashboard again as per general instruction
        
        self.logger.info("--- Clicking 'My E-Service Requests' ---")
        if dashboard_page.is_visible(dashboard_page.link_eservices_requests):
            self.logger.info("Moving mouse to My Requests link...")
            dashboard_page.mouse_hover(dashboard_page.link_eservices_requests)
            time.sleep(2)
            dashboard_page.do_click(dashboard_page.link_eservices_requests)
            
            self.logger.info("Clicked My Requests. Waiting 5 seconds to show the requests table...")
            time.sleep(5)
            
            # Save DOM for table analysis
            with open("eservices_requests_dom.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            self.logger.info("Saved E-Services Requests page DOM.")
            
            assert eservices_page.verify_requests_page(), "My Requests page verification failed"
        else:
            pytest.fail("E-Services 'My Requests' link not found.")
            
        self.logger.info("**** Test_006_EServices Completed Successfully ****")
        time.sleep(2)
