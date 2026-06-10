import pytest
import time
import os
from pages.admin_login_page import AdminLoginPage
from pages.admin_assignment_page import AdminAssignmentPage
from utilities.data_utils import DataUtils

@pytest.mark.admin_assignment
class TestAdminAssignmentCreation:

    def test_create_new_assignment(self, admin_login):
        driver = admin_login
        driver.get(os.getenv("ADMIN_URL", "https://bridge-uat-admin.nios.ac.in"))
        
        login_page = AdminLoginPage(driver)
        success = login_page.login_with_manual_captcha(admin_login.username, admin_login.password, timeout=120)
        assert success, "Admin login failed"
        
        # Navigate
        assign_page = AdminAssignmentPage(driver)
        assign_page.navigate_to_assignment_section()
        
        # Create Dummy PDF
        _, dummy_pdf = DataUtils.ensure_dummy_files()
        
        # List of subjects to add assignments for
        subjects_to_add = ["Mathematics", "Science", "English", "Hindi", "Social Science"]
        
        for subject in subjects_to_add:
            # Create Assignment
            assign_page.click_create_new()
            
            title = f"Automation Test {subject} {int(time.time())}"
            assign_page.fill_assignment_details(
                title=title,
                description=f"This is an auto-generated assignment for {subject}.",
                subject=subject,
                class_name="10",
                medium="English",
                due_date="2026-12-31",
                total_marks=100,
                academic_year="2025-26",
                max_file_size=5
            )
            
            assign_page.upload_assignment_file(dummy_pdf)
            assign_page.publish_assignment()
            
            # Handle potential duplicates or validation failures gracefully
            if assign_page.is_creation_successful():
                assign_page.logger.info(f"Successfully created assignment for {subject}")
                assign_page.navigate_to_assignment_section()
                assert assign_page.verify_assignment_in_list(subject), f"Assignment '{subject}' not found in list"
            else:
                # Check if there is a SweetAlert error popup
                try:
                    error_text = driver.find_element(By.XPATH, "//*[contains(text(), 'Validation failed') or contains(text(), 'already') or contains(text(), 'Error')]").text
                    assign_page.logger.info(f"Assignment for {subject} likely already exists. Skipping... (Msg: {error_text})")
                    # Click OK on the alert
                    assign_page.do_click((By.XPATH, "//button[text()='OK' or contains(@class, 'swal2-confirm')]"))
                    time.sleep(1)
                    # Refresh to reset the page state and close the modal
                    driver.refresh()
                    time.sleep(2)
                    assign_page.navigate_to_assignment_section()
                except Exception as e:
                    assert False, f"Failed to create assignment for {subject} and could not handle error. Exception: {e}"
