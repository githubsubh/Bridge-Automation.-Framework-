import pytest
import time
import os
from pages.login_page import LoginPage
from pages.result_page import ResultPage

@pytest.mark.result
class TestResultRechecking:

    def test_result_rechecking_and_revaluation_flow(self, student_login):
        driver = student_login
        driver.get(os.getenv("FRONTEND_URL", "https://bridge-uat.nios.ac.in") + "/auth/login")
        
        login_page = LoginPage(driver)
        success = login_page.login_with_manual_captcha(student_login.username, student_login.password, timeout=120)
        assert success, "Student login failed"
        
        result_page = ResultPage(driver)
        
        # 1. View Results
        result_page.navigate_to_results()
        if not result_page.is_result_available():
            pytest.skip("Results not yet published. Skipping rechecking/revaluation tests.")
            
        results = result_page.get_all_results()
        assert len(results) > 0, "Results table is empty"
        
        subject_to_test = results[0]["subject"]
        
        # 2. Rechecking
        result_page.navigate_to_rechecking()
        result_page.apply_for_rechecking(subjects=[subject_to_test], reason="Automated rechecking request")
        
        # Handle payment if required
        if result_page.proceed_to_payment():
            # For automation, assume payment bypass or sandbox URL logic would go here
            self.logger.info("Payment step encountered. Skipping for automated test.")
        else:
            assert result_page.is_request_successful(), "Rechecking request failed"
            
        # 3. Revaluation
        result_page.navigate_to_revaluation()
        result_page.apply_for_revaluation(subjects=[subject_to_test], reason="Automated revaluation request")
        
        # Handle payment if required
        if result_page.proceed_to_payment():
            self.logger.info("Payment step encountered. Skipping for automated test.")
        else:
            assert result_page.is_request_successful(), "Revaluation request failed"
            
        # Verify history
        assert result_page.verify_request_exists("revaluation") or result_page.verify_request_exists("rechecking"), "Request not found in history"
