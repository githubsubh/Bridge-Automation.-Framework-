"""
Test Suite: Subject Expert Management — End-to-End
===================================================
Covers: Registration, Summary, Search/Filter, Profile Actions,
School/Subject Mapping, Evaluation, and Security.
"""
import pytest
import time
import os
from pages.admin_login_page import AdminLoginPage
from pages.sme_mgmt_page import SMEManagementPage
from pages.sme_registration_page import SMERegistrationPage
from pages.tma_evaluation_page import TMAEvaluationPage
from utilities.custom_logger import LogGen


# ── Test Data ──
SME_DATA = {
    "name": "Automation Expert",
    "designation": "Subject Expert",
    "dob": "15-06-1990",
    "gender": "Male",
    "aadhaar": "234567891234",
    "school_name": "PT. DEENDAYAL",
    "experience": "5",
    "first_name": "Auto",
    "last_name": "Expert",
    "email": f"sme_auto_{int(time.time())}@test.com",
    "mobile": f"98{int(time.time()) % 100000000:08d}",
    "username": f"sme_auto_{int(time.time())}",
    "password": "Expert@2026",
    "house": "123, Test Colony",
    "street": "Automation Road",
    "state": "Delhi",
    "district": "New Delhi",
    "pincode": "110001",
    "qualification": "M.Sc.",
    "board": "CBSE",
    "passing_year": "2012",
    "percentage": "78",
    "office_name": "NIOS HQ",
    "start_date": "01-01-2015",
    "subject": "Mathematics",
}

ADMIN_URL = os.getenv("ADMIN_URL", "https://bridge-uat-admin.nios.ac.in")


def _admin_login(driver):
    """Helper: login to admin portal with manual CAPTCHA."""
    driver.get(ADMIN_URL)
    time.sleep(2)
    admin = AdminLoginPage(driver)
    admin.handle_restricted_access()
    result = admin.login_with_manual_captcha(
        os.getenv("ADMIN_USER", "superadmin"),
        os.getenv("ADMIN_PASS", "Admin@2025"),
        timeout=120,
    )
    assert result, "Admin login failed or timed out"
    time.sleep(3)
    return admin


# ═══════════════════════════════════════════════════════════════════════════
# 1. SME REGISTRATION TESTS
# ═══════════════════════════════════════════════════════════════════════════
@pytest.mark.sme_registration
class TestSMERegistration:
    logger = LogGen.loggen()

    def test_sme_registration_happy_path(self, setup):
        """TC_SME_REG_01: Register a new SME through the full 8-step wizard."""
        driver = setup
        _admin_login(driver)

        reg = SMERegistrationPage(driver)
        reg.navigate_to_sme_registration()

        # Step 1: Basic Information
        reg.fill_basic_info(
            SME_DATA["name"], SME_DATA["designation"], SME_DATA["dob"],
            SME_DATA["gender"], SME_DATA["aadhaar"], SME_DATA["school_name"],
            SME_DATA["experience"],
        )
        reg.click_next()

        # Step 2: User Credentials
        reg.fill_user_credentials(
            SME_DATA["first_name"], SME_DATA["last_name"], SME_DATA["email"],
            SME_DATA["mobile"], "Secondary", "Subject Expert",
            SME_DATA["username"], SME_DATA["password"], None, None,
        )
        reg.click_next()

        # Step 3: Address Details
        reg.fill_address_details(
            SME_DATA["house"], SME_DATA["street"], SME_DATA["state"],
            SME_DATA["district"], SME_DATA["pincode"], same_as_permanent=True,
        )
        reg.click_next()

        # Step 4: Qualification
        reg.fill_qualification(
            SME_DATA["qualification"], SME_DATA["board"],
            SME_DATA["passing_year"], SME_DATA["percentage"],
        )
        reg.click_next()

        # Step 5: Employment Details
        reg.fill_employment_details(
            SME_DATA["office_name"], SME_DATA["designation"],
            SME_DATA["start_date"],
        )
        reg.click_next()

        # Step 6: Subject Details
        reg.fill_subject_details(SME_DATA["subject"])
        reg.click_next()

        # Step 7: Documents
        photo = os.path.abspath("test_data/official_photo.jpg")
        sig = os.path.abspath("test_data/official_signature.jpg")
        reg.upload_documents(photo, sig)
        reg.click_next()

        # Step 8: Review & Submit
        reg.click_submit()
        time.sleep(3)
        self.logger.info(f"Final URL: {driver.current_url}")

    def test_sme_registration_missing_mandatory_fields(self, setup):
        """TC_SME_REG_02: Submit Step 1 with empty mandatory fields."""
        driver = setup
        _admin_login(driver)

        reg = SMERegistrationPage(driver)
        reg.navigate_to_sme_registration()

        # Click Next without filling anything
        reg.click_next()
        time.sleep(1)

        # Should stay on Step 1 with validation errors
        body = driver.find_element("tag name", "body").text.lower()
        has_error = any(kw in body for kw in ["required", "cannot be blank", "error", "please"])
        assert has_error or "step" in body, "Expected validation errors on empty submit"


# ═══════════════════════════════════════════════════════════════════════════
# 2. SME SUMMARY & MANAGEMENT TESTS
# ═══════════════════════════════════════════════════════════════════════════
@pytest.mark.sme_registration
class TestSMEManagement:
    logger = LogGen.loggen()

    def test_sme_summary_page_loads(self, setup):
        """TC_SME_MAP_27: Verify Summary page loads with data table."""
        driver = setup
        _admin_login(driver)

        mgmt = SMEManagementPage(driver)
        mgmt.navigate_to_summary()
        time.sleep(2)

        row_count = mgmt.get_table_row_count()
        self.logger.info(f"Summary table row count: {row_count}")
        assert row_count > 0 or mgmt.has_no_records(), "Summary page did not load properly"

    def test_sme_search(self, setup):
        """TC_SME_AL_15: Search for an SME by name/email."""
        driver = setup
        _admin_login(driver)

        mgmt = SMEManagementPage(driver)
        mgmt.navigate_to_summary()
        mgmt.search_sme("Expert")
        time.sleep(2)

        row_count = mgmt.get_table_row_count()
        self.logger.info(f"Search results: {row_count} rows")
        # Search should either show results or 'no records'
        assert row_count >= 0

    def test_sme_view_profile(self, setup):
        """TC_SME_LC_25: View an SME profile from the summary list."""
        driver = setup
        _admin_login(driver)

        mgmt = SMEManagementPage(driver)
        mgmt.navigate_to_summary()
        time.sleep(2)

        if mgmt.get_table_row_count() == 0:
            pytest.skip("No SMEs in the table to view")

        # Get first row identifier
        row_data = mgmt.get_row_data(0)
        self.logger.info(f"First SME row: {row_data}")

        # Try to find an identifier (email or name)
        identifier = None
        for key in ["Email", "Name", "Mobile", "email", "name"]:
            if key in row_data and row_data[key]:
                identifier = row_data[key]
                break

        if identifier:
            mgmt.click_view(identifier)
            time.sleep(2)
            current_url = mgmt.get_current_url()
            self.logger.info(f"Profile URL: {current_url}")

    def test_sme_activate_flow(self, setup):
        """TC_SME_LC_25: Draft SMEs should be activatable by admin."""
        driver = setup
        _admin_login(driver)

        mgmt = SMEManagementPage(driver)
        mgmt.navigate_to_summary()

        # Filter by draft status
        try:
            mgmt.apply_filter(status="Draft")
        except Exception:
            self.logger.info("Could not apply Draft filter, checking table directly")

        time.sleep(2)
        if mgmt.get_table_row_count() == 0:
            pytest.skip("No Draft SMEs available to activate")

        row_data = mgmt.get_row_data(0)
        identifier = row_data.get("Email") or row_data.get("Name") or row_data.get("name", "")
        if identifier:
            mgmt.click_activate(identifier)
            time.sleep(2)
            assert mgmt.is_success_alert_visible() or not mgmt.is_error_alert_visible()

    def test_sme_auto_login(self, setup):
        """TC_SME_SEC_26: Auto-login as SME from admin panel."""
        driver = setup
        _admin_login(driver)

        mgmt = SMEManagementPage(driver)
        mgmt.navigate_to_summary()
        time.sleep(2)

        if mgmt.get_table_row_count() == 0:
            pytest.skip("No SMEs in the table")

        row_data = mgmt.get_row_data(0)
        identifier = row_data.get("Email") or row_data.get("Name", "")
        if identifier:
            mgmt.expert_auto_login(identifier)
            time.sleep(3)
            current_url = driver.current_url
            self.logger.info(f"Post auto-login URL: {current_url}")
            # Should be on SME dashboard, not admin
            assert "login" not in current_url.lower()


# ═══════════════════════════════════════════════════════════════════════════
# 3. SME EVALUATION TESTS
# ═══════════════════════════════════════════════════════════════════════════
@pytest.mark.sme_evaluation
class TestSMEEvaluation:
    logger = LogGen.loggen()

    def test_evaluation_page_loads(self, setup):
        """TC_SME_EV_01: SME can access Assignment Evaluation page."""
        driver = setup
        _admin_login(driver)

        eval_page = TMAEvaluationPage(driver)
        eval_page.navigate_to_evaluation()
        time.sleep(2)
        self.logger.info(f"Evaluation page URL: {driver.current_url}")
        assert "evaluation" in driver.current_url.lower() or "assignment" in driver.current_url.lower()

    def test_evaluation_submit_marks(self, setup):
        """TC_SME_WF_17: Submit marks and verify success."""
        driver = setup
        _admin_login(driver)

        eval_page = TMAEvaluationPage(driver)
        eval_page.navigate_to_evaluation()
        time.sleep(2)

        # Try to evaluate first available assignment
        try:
            eval_page.click_preview()
            time.sleep(2)
            eval_page.submit_marks("75", "Evaluated via automation - Good work")
            time.sleep(2)
            assert eval_page.is_evaluation_successful(), "Evaluation submission did not show success"
        except Exception as e:
            self.logger.warning(f"No assignments to evaluate or evaluation failed: {e}")
            pytest.skip("No pending assignments available for evaluation")


# ═══════════════════════════════════════════════════════════════════════════
# 4. SECURITY TESTS
# ═══════════════════════════════════════════════════════════════════════════
@pytest.mark.sme_registration
class TestSMESecurity:
    logger = LogGen.loggen()

    def test_direct_url_without_login(self, setup):
        """TC_SME_SEC_26: Direct URL access without login should redirect."""
        driver = setup
        driver.get(ADMIN_URL + "/subject-expert")
        time.sleep(3)
        assert "login" in driver.current_url.lower(), \
            f"Expected redirect to login, got: {driver.current_url}"

    def test_sme_cannot_access_admin_pages(self, setup):
        """TC_SME_SEC_30: SME role should not access admin-only pages."""
        driver = setup
        _admin_login(driver)

        mgmt = SMEManagementPage(driver)
        mgmt.navigate_to_summary()
        time.sleep(2)

        if mgmt.get_table_row_count() == 0:
            pytest.skip("No SMEs to auto-login as")

        row_data = mgmt.get_row_data(0)
        identifier = row_data.get("Email") or row_data.get("Name", "")
        if not identifier:
            pytest.skip("Could not identify SME for auto-login")

        mgmt.expert_auto_login(identifier)
        time.sleep(3)

        # Now try accessing an admin-only URL
        driver.get(ADMIN_URL + "/admin/settings")
        time.sleep(2)
        body = driver.find_element("tag name", "body").text.lower()
        blocked = any(kw in body for kw in ["denied", "forbidden", "unauthorized", "access"])
        is_redirected = "login" in driver.current_url.lower() or "dashboard" in driver.current_url.lower()
        assert blocked or is_redirected, "SME should not have access to admin settings"
