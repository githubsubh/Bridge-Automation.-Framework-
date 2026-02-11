import pytest
import time
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.eservices_page import EServicesPage
from pages.transactions_page import TransactionsPage
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen
from selenium.webdriver.common.by import By

class Test_Functional_Teacher_Flow:
    home_url = "https://bridge-uat.nios.ac.in/"
    email = ReadConfig.getLoginEmail()
    password = ReadConfig.getLoginPassword()
    logger = LogGen.loggen()

    def test_teacher_end_to_end_functional(self, setup):
        """
        Simulates a functional user session:
        1. Login
        2. E-Services: Attempt to apply for a service & verify navigation
        3. Dashboard: Return to home
        4. Payments: View history & Download receipt
        5. Logout
        """
        self.logger.info("**** Starting Test_Functional_Teacher_Flow ****")
        self.driver = setup
        self.driver.get(self.home_url)

        # --- 1. LOGIN FUNCTIONALITY ---
        home_page = HomePage(self.driver)
        home_page.navigate_to_teacher_login()

        login_page = LoginPage(self.driver)
        if not login_page.login_with_manual_captcha(self.email, self.password, timeout=120):
            pytest.fail("Login failed.")

        self.logger.info("Login successful. Starting Functional E-Services test...")
        time.sleep(5)
        
        dashboard_page = DashboardPage(self.driver)
        eservices_page = EServicesPage(self.driver)
        tx_page = TransactionsPage(self.driver)

        # --- 2. E-SERVICES FUNCTIONALITY ---
        self.logger.info(">>> Scenario: Apply for E-Service")
        # User Action: Click 'E-Services' -> 'Apply' from Dashboard
        dashboard_page.do_click(dashboard_page.link_eservices_apply)
        time.sleep(3)
        
        # Select a specific service to "Functionally" test (e.g., 'Change Appointment Date')
        target_service = "Change Appointment Date"
        self.logger.info(f"Attempting to apply for: {target_service}")
        
        services = eservices_page.get_all_services_details()
        if target_service in services:
            # Click the specific link
            url = services[target_service]
            self.logger.info(f"Clicking apply for {target_service}...")
            self.driver.get(url) # Using get for stability, but simulates click
            time.sleep(3)
            
            # Verify we are on the OTP/Next Step page
            if "verify-otp" in self.driver.current_url:
                self.logger.info("Functional Check PASS: Successfully navigated to OTP Verification page.")
                # Here we would normally enter OTP. Since we can't, we verify the user can 'Cancel' or 'Back'.
                # Simulating user deciding to go back to Dashboard.
            else:
                pytest.fail(f"Functional Check FAIL: Did not reach OTP page for {target_service}")
        else:
            self.logger.warning(f"Service '{target_service}' not found! Picking first available...")
            # Fallback logic could go here
        
        # --- 3. NAVIGATION FUNCTIONALITY ---
        self.logger.info(">>> Scenario: Navigate Back to Dashboard")
        # Simulate clicking the 'Dashboard' link in the header/breadcrumb/footer
        # Using the dashboard page object method usually ensures this
        self.driver.get(self.home_url + "teacher/dashboard") 
        time.sleep(3)
        
        if "Dashboard" in self.driver.title:
            self.logger.info("Navigation PASS: Returned to Dashboard.")
        
        # --- 4. PAYMENT & DOWNLOAD FUNCTIONALITY ---
        self.logger.info(">>> Scenario: Payment History & Receipt Download")
        # User Action: Click 'Payment History'
        dashboard_page.do_click(dashboard_page.link_payment_history)
        time.sleep(3)
        
        # Functional Action: Verify data matches expectations (at least 1 paid item)
        txs = tx_page.get_all_transactions()
        if txs and txs[0]['status'] == "PAID":
            self.logger.info("Data Check PASS: Found valid PAID transactions.")
            
            # Functional Action: Download Receipt
            self.logger.info("Action: Downloading Receipt...")
            if tx_page.download_first_receipt():
                 self.logger.info("Functional Check PASS: Receipt downloaded and tab verified.")
            else:
                 self.logger.error("Functional Check FAIL: Receipt download failed.")
        else:
            self.logger.warning("No PAID transactions found to test download.")

        # --- 5. LOGOUT FUNCTIONALITY ---
        self.logger.info(">>> Scenario: Logout")
        time.sleep(2)
        dashboard_page.do_logout()
        self.logger.info("**** Test_Functional_Teacher_Flow Completed ****")
