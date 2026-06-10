import pytest
import time
from datetime import datetime, timedelta
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.admin_login_page import AdminLoginPage
from pages.admin_exam_fee_schedule_page import AdminExamFeeSchedulePage
from pages.exam.exam_registration_page import ExamRegistrationPage
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen

class Test_Exam_Date_Logic:
    logger = LogGen.loggen()
    
    backend_conf = ReadConfig.getBackendConfig()
    teacher_conf = {
        "url": ReadConfig.getLoginURL(),
        "email": ReadConfig.getLoginEmail(),
        "password": ReadConfig.getLoginPassword()
    }

    @pytest.mark.exam_logic
    def test_exam_tile_visibility_logic(self, setup):
        self.logger.info("**** Starting Test_Exam_Tile_Visibility_Logic ****")
        driver = setup
        
        # 1. Backend: Set dates to PAST (Registration Closed)
        self.logger.info("Step 1: Closing registration in backend...")
        driver.get(self.backend_conf["url"])
        admin_login = AdminLoginPage(driver)
        admin_login.handle_restricted_access()
        success = admin_login.login_with_manual_captcha(self.backend_conf["username"], self.backend_conf["password"])
        assert success, "Admin login failed or timed out."
        time.sleep(3)
        
        admin_schedule = AdminExamFeeSchedulePage(driver)
        admin_schedule.navigate_to_exam_fee_schedule()
        
        # Set dates to 1 month ago
        past_date = (datetime.now() - timedelta(days=30)).strftime("%d-%m-%Y")
        admin_schedule.set_exam_dates(past_date, past_date, past_date, past_date)
        
        # 2. Teacher Portal: Verify tile DISAPPEARS or shows CLOSED
        self.logger.info("Step 2: Verifying tile status in teacher portal (Should be closed/hidden)...")
        driver.get(self.teacher_conf["url"])
        login_page = LoginPage(driver)
        login_page.handle_restricted_access()
        login_page.login_with_manual_captcha(self.teacher_conf["email"], self.teacher_conf["password"])
        
        dashboard = DashboardPage(driver)
        exam_reg = ExamRegistrationPage(driver)
        
        tile_visible = dashboard.is_visible(exam_reg.EXAM_REG_BOX)
        self.logger.info(f"Exam Registration Tile visibility: {tile_visible}")
        
        # Note: Depending on requirement, it might disappear or show a 'Closed' message
        # For now, let's assume it should not be clickable for registration
        if tile_visible:
            reg_link_visible = dashboard.is_visible(exam_reg.REGISTER_LINK)
            assert not reg_link_visible, "Exam Registration 'Register' link is visible even when registration is closed in backend!"
        
        # 3. Backend: Set dates to ACTIVE (Registration Open)
        self.logger.info("Step 3: Opening registration in backend...")
        driver.get(self.backend_conf["url"])
        # (Already logged in or might need re-login depending on session)
        if "login" in driver.current_url:
            success = admin_login.login_with_manual_captcha(self.backend_conf["username"], self.backend_conf["password"])
            assert success, "Admin re-login failed."
            
        admin_schedule.navigate_to_exam_fee_schedule()
        
        today = datetime.now().strftime("%d-%m-%Y")
        future_date = (datetime.now() + timedelta(days=30)).strftime("%d-%m-%Y")
        admin_schedule.set_exam_dates(today, future_date, future_date, future_date)
        
        # 4. Teacher Portal: Verify tile APPEARS
        self.logger.info("Step 4: Verifying tile status in teacher portal (Should be open)...")
        driver.get(self.teacher_conf["url"])
        # (Session might still be active)
        if "login" in driver.current_url:
            login_page.login_with_manual_captcha(self.teacher_conf["email"], self.teacher_conf["password"])
            
        tile_visible = dashboard.is_visible(exam_reg.EXAM_REG_BOX)
        reg_link_visible = dashboard.is_visible(exam_reg.REGISTER_LINK)
        
        assert tile_visible, "Exam Registration tile is NOT visible when registration is open!"
        assert reg_link_visible, "Exam Registration 'Register' link is NOT visible when registration is open!"
        
        # 5. Near Expiry Warning Check
        self.logger.info("Step 5: Testing near-expiry warning...")
        driver.get(self.backend_conf["url"])
        if "login" in driver.current_url:
            success = admin_login.login_with_manual_captcha(self.backend_conf["username"], self.backend_conf["password"])
            assert success, "Admin re-login for warning check failed."
        admin_schedule.navigate_to_exam_fee_schedule()
        
        # Set end date to tomorrow
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%d-%m-%Y")
        admin_schedule.set_exam_dates(today, tomorrow, tomorrow, tomorrow)
        
        driver.get(self.teacher_conf["url"])
        if "login" in driver.current_url:
            login_page.login_with_manual_captcha(self.teacher_conf["email"], self.teacher_conf["password"])
            
        exam_reg.navigate_to_exam_registration()
        warning = exam_reg.get_dynamic_warning()
        if warning:
            self.logger.info(f"Verified dynamic warning: {warning}")
        else:
            self.logger.warning("No dynamic warning found for near-expiry date. This might be a bug if expected.")
        
        self.logger.info("**** Finished Test_Exam_Date_Logic ****")
