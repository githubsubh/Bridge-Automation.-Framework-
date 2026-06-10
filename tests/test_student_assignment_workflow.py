import pytest
import time
import os
from pages.login_page import LoginPage
from pages.student_assignment_page import StudentAssignmentPage
from utilities.data_utils import DataUtils

@pytest.mark.student_assignment
class TestStudentAssignmentWorkflow:

    def test_student_assignment_upload_and_reupload(self, student_login):
        driver = student_login
        driver.get(os.getenv("FRONTEND_URL", "https://bridge-uat.nios.ac.in") + "/auth/login")
        
        login_page = LoginPage(driver)
        success = login_page.login_with_manual_captcha(student_login.username, student_login.password, timeout=120)
        assert success, "Student login failed"
        
        assignment_page = StudentAssignmentPage(driver)
        assignment_page.navigate_to_my_assignments()
        
        # Ensure dummy files exist
        _, dummy_pdf = DataUtils.ensure_dummy_files()
        subject = "Mathematics"
        
        # Download (if available)
        assignment_page.download_assignment(subject)
        
        # Initial Upload
        if assignment_page.is_upload_allowed(subject):
            assignment_page.click_upload_action(subject)
            assignment_page.submit_assignment(subject, dummy_pdf, direct_upload=True)
            assert assignment_page.is_submission_successful(), "Initial upload failed"
            
            # Verify Status changed to Submitted
            status = assignment_page.get_assignment_status(subject)
            assert "Submitted" in status, f"Status not Submitted, got {status}"
            
            # Re-upload
            if assignment_page.is_upload_allowed(subject):
                assignment_page.click_upload_action(subject)
                assignment_page.submit_assignment(subject, dummy_pdf, direct_upload=True)
                assert assignment_page.is_submission_successful(), "Re-upload failed"
        else:
            pytest.skip("Upload/Re-upload is not allowed for the given subject (deadline passed or not allocated).")

