import pytest
import time
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen
from selenium.webdriver.common.by import By

class Test_Explore_Grievances_Results:
    home_url = "https://bridge-uat.nios.ac.in/"
    email = ReadConfig.getLoginEmail()
    password = ReadConfig.getLoginPassword()
    logger = LogGen.loggen()

    def test_explore_new_modules(self, setup):
        self.logger.info("**** Starting Test_Explore_Grievances_Results ****")
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

        # 2. Explore Results
        self.logger.info("--- Exploring Results Section ---")
        if dashboard_page.verify_results_section():
            self.logger.info("Results section verified. Clicking 'Public Exam Results'...")
            dashboard_page.do_click(dashboard_page.link_public_exam_results)
            time.sleep(5)
            # Find if it opened a new tab or stayed
            self.logger.info(f"Current URL after Results Click: {self.driver.current_url}")
            with open("results_page_dom.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            
            # Navigate back if it stayed on same page
            if "dashboard" not in self.driver.current_url:
                self.driver.get(self.home_url + "teacher/dashboard")
                time.sleep(3)

        # 3. Explore Grievances
        self.logger.info("--- Exploring Grievances Section ---")
        if dashboard_page.verify_grievances_section():
            self.logger.info("Grievances section verified. Clicking 'Submit'...")
            
            # The grievance link is an external anchor, it might open in new tab
            original_window = self.driver.current_window_handle
            dashboard_page.do_click(dashboard_page.link_submit_grievance)
            time.sleep(5)
            
            # Check for new window
            for handle in self.driver.window_handles:
                if handle != original_window:
                    self.driver.switch_to.window(handle)
                    self.logger.info(f"Switched to Grievance Window: {self.driver.current_url}")
                    with open("grievance_portal_dom.html", "w", encoding="utf-8") as f:
                        f.write(self.driver.page_source)
                    self.driver.close()
                    self.driver.switch_to.window(original_window)
                    self.logger.info("Back to Home Dashboard.")
                    break
            else:
                self.logger.info(f"No new window opened. Current URL: {self.driver.current_url}")
                if "grs.nios.ac.in" in self.driver.current_url:
                    with open("grievance_portal_dom.html", "w", encoding="utf-8") as f:
                        f.write(self.driver.page_source)
                    self.driver.get(self.home_url + "teacher/dashboard")
                    time.sleep(3)

        self.logger.info("**** Exploration Completed ****")
