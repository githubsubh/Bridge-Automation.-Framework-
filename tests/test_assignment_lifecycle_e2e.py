import pytest
import time
from pages.admin_login_page import AdminLoginPage
from pages.sme_mgmt_page import SMEManagementPage
from pages.assignment_allocation_page import AssignmentAllocationPage
from pages.tma_evaluation_page import TMAEvaluationPage
from pages.student_assignment_page import StudentAssignmentPage
from pages.login_page import LoginPage # Student Login
import os

@pytest.mark.lifecycle
class TestAssignmentLifecycleE2E:
    
    # Environment Details
    ADMIN_URL = "https://bridge-uat-admin.nios.ac.in"
    STUDENT_URL = "https://bridge-uat.nios.ac.in/auth/login"
    
    # Test Data Setup
    SUBJECTS = ["Mathematics", "Physics", "Chemistry", "Biology", "English", "Economics", "History"]
    EXPERT_EMAIL = "expert_a@bridge.com"
    STUDENT_USER = "student_test_01"
    STUDENT_PASS = "Password@123"
    DUMMY_PDF = os.path.abspath("dummy_assignment.pdf")

    def test_full_assignment_lifecycle(self, setup):
        driver = setup
        # 1. Backend: Allocation to Expert
        admin_login = AdminLoginPage(driver)
        sme_mgmt = SMEManagementPage(driver)
        allocation_page = AssignmentAllocationPage(driver)
        
        driver.get(self.ADMIN_URL)
        admin_login.login("Superadmin", "Admin@2025")
        time.sleep(5) # Wait for dashboard to load
        
        # Clear any restricted access prompts
        allocation_page.handle_restricted_access()
        
        print("Navigating to Expert Allocation...")
        allocation_page.navigate_to_allocation()


        
        for subject in self.SUBJECTS:
            allocation_page.allocate_assignments("PT. DEENDAYAL UPADHYAY GOVT. MODEL I.C MANKAIDA", subject, "Expert_A")
            assert allocation_page.is_allocation_successful(), f"Allocation failed for {subject}"

        # 2. Expert: Evaluation via Auto-login
        sme_mgmt.navigate_to_summary()
        sme_mgmt.expert_auto_login(self.EXPERT_EMAIL)
        
        eval_page = TMAEvaluationPage(driver)
        eval_page.navigate_to_evaluation()
        
        # Evaluate one assignment as a sample
        eval_page.click_preview()
        eval_page.submit_marks("85", "Good work - Automated Test")
        
        # Verify status
        status = eval_page.get_assignment_status("MATH_2025_01") 
        assert status == "Evaluated", f"Expected status 'Evaluated' but got '{status}'"

        # 3. Student Dashboard Verification
        driver.get(self.STUDENT_URL)
        
        student_login = LoginPage(driver)
        student_dashboard = StudentAssignmentPage(driver)
        
        student_login.login(self.STUDENT_USER, self.STUDENT_PASS)
        student_dashboard.navigate_to_my_assignments()
        
        current_status = student_dashboard.get_assignment_status("Mathematics")
        assert current_status in ["Evaluated", "Approved", "Published"], f"Status sync failed for student. Current: {current_status}"

        print("Assignment Lifecycle E2E Test Passed Successfully.")
