import pytest
import time
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen

class Test_003_DashboardFeatures:
    # Read config
    login_url = ReadConfig.getLoginURL()
    email = ReadConfig.getLoginEmail()
    password = ReadConfig.getLoginPassword()
    logger = LogGen.loggen()
    
    def test_dashboard_features(self, setup):
        self.logger.info("**** Starting Test_003_DashboardFeatures ****")
        self.driver = setup
        self.driver.get(self.login_url)
        
        # 1. Login Phase
        login_page = LoginPage(self.driver)
        self.logger.info("Logging in to access Dashboard...")
        if not login_page.login_with_manual_captcha(self.email, self.password, timeout=120):
            pytest.fail("Login failed, cannot test dashboard.")
            
        # 2. Dashboard Verification Phase
        dashboard_page = DashboardPage(self.driver)
        
        # Verify Features One by One
        self.logger.info("--- 1. Study Material Check ---")
        assert dashboard_page.verify_study_material(), "Study Material Section Verification Failed"
        
        self.logger.info("--- 2. E-Services Check ---")
        assert dashboard_page.verify_eservices(), "E-Services Section Verification Failed"
        
        self.logger.info("--- 3. Payment Status Check ---")
        assert dashboard_page.verify_payment_status(), "Payment Status Section Verification Failed"
        
        self.logger.info("--- 4. My Documents Check ---")
        assert dashboard_page.verify_my_documents(), "My Documents Section Verification Failed"
        
        self.logger.info("--- 5. Print Section Check ---")
        assert dashboard_page.verify_print_section(), "Print Section Verification Failed"
        
        self.logger.info("--- 6. Results Section Check ---")
        assert dashboard_page.verify_results_section(), "Results Section Verification Failed"
        
        self.logger.info("--- 7. Grievances Section Check ---")
        assert dashboard_page.verify_grievances_section(), "Grievances Section Verification Failed"
        
        self.logger.info("--- 8. Workflow Check ---")
        assert dashboard_page.verify_workflow(), "Workflow/Registration Steps Verification Failed"
        
        self.logger.info("--- 9. Logout Check ---")
        dashboard_page.do_logout()
        
        self.logger.info("**** Test_003_DashboardFeatures Passed Successfully ****")
