import pytest
import time
import os
from pages.login_page import LoginPage
from pages.student_assignment_page import StudentAssignmentPage

@pytest.mark.assignment_status
class TestAssignmentStatusVerification:

    def test_verify_assignment_status_and_marks(self, student_login):
        driver = student_login
        driver.get(os.getenv("FRONTEND_URL", "https://bridge-uat.nios.ac.in") + "/auth/login")
        
        login_page = LoginPage(driver)
        success = login_page.login_with_manual_captcha(student_login.username, student_login.password, timeout=120)
        assert success, "Student login failed"
        
        assignment_page = StudentAssignmentPage(driver)
        assignment_page.navigate_to_my_assignments()
        
        subject = "Mathematics"
        
        status = assignment_page.get_assignment_status(subject)
        marks = assignment_page.get_assignment_marks(subject)
        
        # Valid statuses
        valid_statuses = ["Pending", "Submitted", "Evaluated", "Approved", "Published"]
        
        # Check if status is one of the valid statuses
        is_valid = any(s.lower() in status.lower() for s in valid_statuses)
        assert is_valid or status == "", f"Unknown assignment status: {status}"
        
        if "Evaluated" in status or "Published" in status:
            assert marks != "", f"Marks should be visible for evaluated/published status. Status: {status}"
        
        if "Published" in status:
            is_published = assignment_page.verify_result_published(subject)
            assert is_published, "Status is Published but result is not visible in My Results"
