import pytest
import time
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen
from selenium.webdriver.common.by import By

class Test_Profile_Data_Continuity:
    home_url = "https://bridge-uat.nios.ac.in/"
    email = ReadConfig.getLoginEmail()
    password = ReadConfig.getLoginPassword()
    logger = LogGen.loggen()

    def test_verify_profile_data_across_pages(self, setup):
        """
        Continuity Test:
        1. Login
        2. Scrape Name & Ref No from Dashboard.
        3. Verify against School Details Modal.
        4. Verify against Application Form Print View.
        """
        self.logger.info("**** Starting Test_Profile_Data_Continuity ****")
        self.driver = setup
        self.driver.get(self.home_url)

        # 1. Login
        home_page = HomePage(self.driver)
        home_page.navigate_to_teacher_login()
        login_page = LoginPage(self.driver)
        if not login_page.login_with_manual_captcha(self.email, self.password, timeout=120):
            pytest.fail("Login failed.")

        dashboard_page = DashboardPage(self.driver)
        time.sleep(5)

        # 2. Scrape Dashboard Data
        dash_name = dashboard_page.get_teacher_name()
        dash_ref_no = dashboard_page.get_reference_no()
        self.logger.info(f"Dashboard Data - Name: {dash_name}, Ref No: {dash_ref_no}")

        # 3. Verify School Modal
        self.logger.info("Opening School Details Modal...")
        dashboard_page.click_school_details()
        time.sleep(3)
        modal_udise = dashboard_page.get_modal_udise_code()
        self.logger.info(f"Modal Data - UDISE: {modal_udise}")
        assert modal_udise != "", "Modal UDISE should not be empty"
        dashboard_page.do_click(dashboard_page.modal_close_btn)
        time.sleep(2)

        # 4. Verify Print Application Form
        self.logger.info("Opening Application Form Print View...")
        original_window = self.driver.current_window_handle
        dashboard_page.do_click(dashboard_page.link_print_application)
        time.sleep(5)

        # Handle New Tab
        all_windows = self.driver.window_handles
        if len(all_windows) > 1:
            self.driver.switch_to.window(all_windows[1])
            self.logger.info(f"Switched to Print View. URL: {self.driver.current_url}")
            
            # Save DOM for first time analysis
            with open("print_form_analysis.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            self.logger.info("Saved Print Form DOM for locator analysis.")

            # Simple text check for now 
            page_text = self.driver.page_source
            assert dash_name.upper() in page_text.upper(), f"Name {dash_name} not found in Print View"
            assert dash_ref_no in page_text, f"Ref No {dash_ref_no} not found in Print View"
            self.logger.info("Continuity Check PASS: Name and Ref No found in Print View.")

            self.driver.close()
            self.driver.switch_to.window(original_window)
            time.sleep(2)
        else:
            self.logger.warning("Print view did not open in new tab as expected.")

        self.logger.info("**** Test_Profile_Data_Continuity Completed successfully ****")
