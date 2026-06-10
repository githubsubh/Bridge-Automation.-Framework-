# -*- coding: utf-8 -*-
"""
End‑to‑End Assignment Workflow Test
===================================

This test covers the full lifecycle of an assignment:
1️⃣  Backend – Admin creates & publishes the assignment.
2️⃣  Frontend – Teacher (acting as a student) submits the assignment.
3️⃣  Simulated wait (configurable, default 2 days).
4️⃣  Backend – SME registration / mapping (if required) and allocation.
5️⃣  SME evaluates the assignment, enters marks & remarks.
6️⃣  Final verification – Teacher checks the assignment status & marks.

All required fixtures (admin_login, teacher_login, student_login,
        sme_login, base_url, wait_config) already exist in the framework.
"""

import time
import pytest
import os

from pages.admin_login_page import AdminLoginPage
from pages.assignment_allocation_page import AssignmentAllocationPage
from pages.student_assignment_page import StudentAssignmentPage
from pages.teacher_page import TeacherPage
from pages.sme_page import SmePage

# ----------------------------------------------------------------------
# Test data – can be externalised later (CSV/JSON) for data‑driven runs
# ----------------------------------------------------------------------
ASSIGNMENT_DATA = {
    "title": "Automation Assignment – Full Workflow",
    "description": "Validate end‑to‑end assignment flow using Selenium.",
    "subject": "Mathematics",
    "class_name": "10",
    "section": "A",
    "due_date": "2026-12-31",
    "total_marks": "100",
    "upload_file": "C:/AutomationProjects/Bridge-Automation.-Framework-/test_data/sample_assignment.pdf",
    "expert_name": "John Doe",
    "marks_obtained": "85",
    "remarks": "Good work, minor calculation errors.",
}

@pytest.mark.full_assignment_workflow

def test_assignment_full_workflow(
    admin_login,
    teacher_login,
    student_login,
    sme_login,
    admin_url,
    frontend_url,
    wait_config,
):
    """End‑to‑end test for creating, submitting, allocating and evaluating an assignment."""

    # ------------------------------------------------------------------
    # 1️⃣ Admin creates the assignment
    # ------------------------------------------------------------------
    os.environ["SKIP_CAPTCHA"] = "true"
    admin_driver.get("https://bridge-uat-admin.nios.ac.in/auth/login")
    AdminLoginPage(admin_driver).login(
        username=admin_login.username, password=admin_login.password
    )
    allocation_page = AssignmentAllocationPage(admin_driver)
    allocation_page.navigate_to_allocation()
    # Create a single assignment for Mathematics
    subject = "Mathematics"
    allocation_page.create_and_publish_assignment(
        title=f"{ASSIGNMENT_DATA["title"]} - {subject}",
        description=ASSIGNMENT_DATA["description"],
        subject=subject,
        class_name=ASSIGNMENT_DATA["class_name"],
        section=ASSIGNMENT_DATA["section"],
        due_date=ASSIGNMENT_DATA["due_date"],
        total_marks=ASSIGNMENT_DATA["total_marks"],
    )
    assert allocation_page.is_creation_successful(), "Admin assignment creation failed"
os.environ["SKIP_CAPTCHA"] = "false"

    # ------------------------------------------------------------------
    # 2️⃣ Teacher (as Student) submits the assignment – manual captcha
    # ------------------------------------------------------------------

teacher_driver = teacher_login
    teacher_driver.get("https://bridge-uat.nios.ac.in/auth/login")
    # Manual captcha will be required here – pause for user
    AdminLoginPage(teacher_driver).login(
        username=teacher_login.username, password=teacher_login.password
    )
    TeacherPage(teacher_driver).switch_to_student_view()
    student_page = StudentAssignmentPage(teacher_driver)
    student_page.navigate_to_my_assignments()
    student_page.submit_assignment(
        subject_name=ASSIGNMENT_DATA["subject"],
        file_path=ASSIGNMENT_DATA["upload_file"],
    )
    status = student_page.get_assignment_status(ASSIGNMENT_DATA["subject"])
    assert "Submitted" in status, f"Submission status unexpected: {status}"


    # ------------------------------------------------------------------
    # 3️⃣ Simulated wait (2 days)
    # ------------------------------------------------------------------
    simulated_days = wait_config.get("assignment_wait_days", 2)
    time.sleep(simulated_days * wait_config.get("seconds_per_day", 1))

    # ------------------------------------------------------------------
    # 4️⃣ SME handling – allocate assignment to SME
    # ------------------------------------------------------------------
    sme_driver = sme_login
    sme_driver.get(f"{admin_url}/auth/login")
    AdminLoginPage(sme_driver).login(
        username=sme_login.username, password=sme_login.password
    )
    allocation_page = AssignmentAllocationPage(sme_driver)
    allocation_page.navigate_to_allocation()
    allocation_page.allocate_assignments(
        school="National Institute of Open Schooling",
        subject=ASSIGNMENT_DATA["subject"],
        expert_name=ASSIGNMENT_DATA["expert_name"],
    )
    assert allocation_page.is_allocation_successful(), "SME allocation failed"

    # ------------------------------------------------------------------
    # 5️⃣ SME evaluates the assignment
    # ------------------------------------------------------------------
    sme_page = SmePage(sme_driver)
    sme_page.navigate_to_evaluation()
    sme_page.evaluate_assignment(
        subject_name=ASSIGNMENT_DATA["subject"],
        marks=ASSIGNMENT_DATA["marks_obtained"],
        remarks=ASSIGNMENT_DATA["remarks"],
    )
    assert sme_page.is_evaluation_successful(), "SME evaluation failed"

    # ------------------------------------------------------------------
    # 6️⃣ Final verification – Teacher checks marks and status
    # ------------------------------------------------------------------
    teacher_driver.get(f"{frontend_url}/teacher")
    TeacherPage(teacher_driver).switch_to_student_view()
    student_page.navigate_to_my_assignments()
    final_status = student_page.get_assignment_status(ASSIGNMENT_DATA["subject"])
    assert "Evaluated" in final_status, f"Final status not evaluated: {final_status}"
    marks_displayed = student_page.get_assignment_marks(ASSIGNMENT_DATA["subject"])
    assert marks_displayed == ASSIGNMENT_DATA["marks_obtained"], (
        f"Marks mismatch – expected {ASSIGNMENT_DATA['marks_obtained']}, got {marks_displayed}"
    )
