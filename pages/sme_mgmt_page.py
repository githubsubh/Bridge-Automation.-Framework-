"""
SME Management Page — Page Object for Subject Expert Management on Admin Portal.
================================================================================
Covers: Summary listing, Search/Filter, Profile Actions (View/Edit/Activate/
Suspend/Auto-Login), Assignment Stats, and Bulk Operations.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import time


class SMEManagementPage(BasePage):
    """Page Object for the Subject Expert Management module on Admin Portal."""

    # ── Sidebar Navigation ──
    SUBJECT_EXPERTS_MENU = (By.XPATH, "//a[contains(.,'Subject Experts')]")
    ADD_SME_SUBMENU = (By.XPATH, "//a[contains(.,'Add Subject Expert')]")
    SUMMARY_SUBMENU = (
        By.XPATH,
        "//a[contains(@href, 'subject-expert') and contains(.,'Summary')]"
        " | //ul[contains(@class, 'submenu')]//a[contains(., 'Summary')]",
    )

    # ── Summary Page — Search & Filter ──
    SEARCH_FIELD = (By.XPATH, "//input[@type='search']")
    FILTER_BUTTON = (By.XPATH, "//button[contains(.,'Filter')] | //a[contains(.,'Filter')]")
    STATUS_FILTER = (By.ID, "status_chosen")
    DISTRICT_FILTER = (By.ID, "district_id_chosen")
    SUBJECT_FILTER = (By.ID, "subject_id_chosen")
    APPLY_FILTER_BTN = (By.XPATH, "//button[contains(text(),'Apply') or contains(text(),'Search')]")
    RESET_FILTER_BTN = (By.XPATH, "//button[contains(text(),'Reset') or contains(text(),'Clear')]")

    # ── Summary Table ──
    TABLE_ROWS = (By.XPATH, "//table[contains(@class,'table')]//tbody/tr")
    TABLE_HEADERS = (By.XPATH, "//table[contains(@class,'table')]//thead/tr/th")
    NO_RECORDS = (By.XPATH, "//*[contains(text(),'No records') or contains(text(),'No data') or contains(text(),'No results')]")
    PAGINATION_NEXT = (By.XPATH, "//a[contains(@class,'page-link') and contains(.,'Next')]")
    PAGINATION_PREV = (By.XPATH, "//a[contains(@class,'page-link') and contains(.,'Previous')]")
    PAGINATION_INFO = (By.XPATH, "//*[contains(@class,'dataTables_info')]")

    # ── Row Action Buttons (dynamic — use format with SME email/ID) ──
    VIEW_ICON_XPATH = "//td[contains(text(), '{identifier}')]/ancestor::tr//a[contains(@title, 'View') or contains(@class, 'view')]"
    EDIT_ICON_XPATH = "//td[contains(text(), '{identifier}')]/ancestor::tr//a[contains(@title, 'Edit') or contains(@class, 'edit')]"
    ACTIVATE_ICON_XPATH = "//td[contains(text(), '{identifier}')]/ancestor::tr//a[contains(@title, 'Activate') or contains(@title, 'Approve')]"
    SUSPEND_ICON_XPATH = "//td[contains(text(), '{identifier}')]/ancestor::tr//a[contains(@title, 'Suspend') or contains(@title, 'Deactivate')]"
    AUTO_LOGIN_ICON_XPATH = "//td[contains(text(), '{identifier}')]/ancestor::tr//a[contains(@title, 'Auto Login') or contains(@title, 'Login')]"
    DELETE_ICON_XPATH = "//td[contains(text(), '{identifier}')]/ancestor::tr//a[contains(@title, 'Delete') or contains(@class, 'delete')]"

    # ── Profile / Detail View ──
    PROFILE_NAME = (By.XPATH, "//*[contains(@class, 'profile-name') or contains(@class, 'card-title')]")
    PROFILE_STATUS_BADGE = (By.XPATH, "//span[contains(@class, 'badge')]")
    PROFILE_SUBJECTS = (By.XPATH, "//td[contains(text(), 'Subject')]/following-sibling::td | //label[contains(text(), 'Subject')]/..//span")
    PROFILE_SCHOOL_LIST = (By.XPATH, "//td[contains(text(), 'School')]/following-sibling::td | //label[contains(text(), 'School')]/..//span")
    BACK_TO_LIST_BTN = (By.XPATH, "//a[contains(.,'Back') or contains(.,'List')] | //button[contains(.,'Back')]")

    # ── Edit Form Fields ──
    EDIT_NAME_FIELD = (By.NAME, "name")
    EDIT_DESIGNATION_FIELD = (By.NAME, "designation")
    EDIT_MOBILE_FIELD = (By.NAME, "mobile_no")
    EDIT_EMAIL_FIELD = (By.NAME, "email")
    EDIT_PAN_FIELD = (By.NAME, "pan_no")
    EDIT_AADHAAR_FIELD = (By.NAME, "aadhaar_no")
    EDIT_SAVE_BTN = (By.XPATH, "//button[contains(text(),'Save') or contains(text(),'Update')]")

    # ── School / Subject Mapping ──
    MAP_SCHOOL_BTN = (By.XPATH, "//button[contains(.,'Map School') or contains(.,'Add School')]")
    MAP_SUBJECT_BTN = (By.XPATH, "//button[contains(.,'Map Subject') or contains(.,'Add Subject')]")
    SCHOOL_MAPPING_DROPDOWN = (By.ID, "study_centre_id_chosen")
    SUBJECT_MAPPING_DROPDOWN = (By.ID, "subject_mapping_id_chosen")
    SAVE_MAPPING_BTN = (By.XPATH, "//button[contains(text(),'Save Mapping') or contains(text(),'Map')]")
    UNLINK_SCHOOL_XPATH = "//td[contains(text(), '{school_name}')]/following-sibling::td//button[contains(.,'Remove') or contains(.,'Unlink')]"
    SELECT_ALL_SCHOOLS = (By.ID, "select_all_schools")

    # ── Stats / Dashboard Counters ──
    TOTAL_SME_COUNT = (By.XPATH, "//*[contains(@class,'stat') or contains(@class,'count')]//*[contains(text(),'Total')]/..//span | //*[contains(text(),'Total SME')]/..//strong")
    ACTIVE_SME_COUNT = (By.XPATH, "//*[contains(text(),'Active')]/..//strong | //*[contains(text(),'Active')]/..//span")
    DRAFT_SME_COUNT = (By.XPATH, "//*[contains(text(),'Draft')]/..//strong | //*[contains(text(),'Draft')]/..//span")

    # ── Confirmation Modals ──
    CONFIRM_YES_BTN = (By.XPATH, "//button[contains(text(),'Yes') or contains(text(),'Confirm') or contains(@class,'swal2-confirm')]")
    CONFIRM_NO_BTN = (By.XPATH, "//button[contains(text(),'No') or contains(text(),'Cancel') or contains(@class,'swal2-cancel')]")

    # ── Alerts ──
    SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert-success, .swal2-success, .swal2-popup.swal2-icon-success")
    ERROR_ALERT = (By.CSS_SELECTOR, ".alert-danger, .alert-error, .swal2-error")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".help-block, .invalid-feedback, .field-error, .text-danger")

    def __init__(self, driver):
        super().__init__(driver)

    # ═══════════════════════════════════════════════════════════════════════
    # NAVIGATION
    # ═══════════════════════════════════════════════════════════════════════
    def navigate_to_add_sme(self):
        """Navigate to Subject Experts -> Add Subject Expert."""
        self.logger.info("Navigating to Add Subject Expert...")
        self.do_click(self.SUBJECT_EXPERTS_MENU)
        time.sleep(1)
        self.do_click(self.ADD_SME_SUBMENU)
        time.sleep(2)

    def navigate_to_summary(self):
        """Navigate to Subject Experts -> Summary listing."""
        self.logger.info("Navigating to Subject Expert Summary...")
        self.do_click(self.SUBJECT_EXPERTS_MENU)
        time.sleep(1)
        self.do_click(self.SUMMARY_SUBMENU)
        time.sleep(2)

    # ═══════════════════════════════════════════════════════════════════════
    # SEARCH & FILTER
    # ═══════════════════════════════════════════════════════════════════════
    def search_sme(self, query):
        """Searches for an SME in the summary table using the global search."""
        self.logger.info(f"Searching for SME: '{query}'...")
        self.do_send_keys(self.SEARCH_FIELD, query)
        time.sleep(2)

    def apply_filter(self, status=None, district=None, subject=None):
        """Opens the filter panel and applies given filters."""
        self.logger.info(f"Applying filters — status={status}, district={district}, subject={subject}")
        try:
            self.do_click(self.FILTER_BUTTON)
            time.sleep(1)
        except Exception:
            self.logger.info("Filter panel may already be open or inline.")

        if status:
            self.select_chosen_option(self.STATUS_FILTER, status)
        if district:
            self.select_chosen_option(self.DISTRICT_FILTER, district)
        if subject:
            self.select_chosen_option(self.SUBJECT_FILTER, subject)

        self.do_click(self.APPLY_FILTER_BTN)
        time.sleep(2)

    def reset_filters(self):
        """Resets all active filters."""
        try:
            self.do_click(self.RESET_FILTER_BTN)
            time.sleep(1)
        except Exception:
            self.logger.warning("Reset filter button not found. Refreshing page.")
            self.driver.refresh()
            time.sleep(2)

    # ═══════════════════════════════════════════════════════════════════════
    # TABLE OPERATIONS
    # ═══════════════════════════════════════════════════════════════════════
    def get_table_row_count(self):
        """Returns the number of data rows currently visible in the table."""
        rows = self.driver.find_elements(*self.TABLE_ROWS)
        count = len(rows)
        self.logger.info(f"Table row count: {count}")
        return count

    def has_no_records(self):
        """Returns True if 'No records' message is displayed."""
        return self.is_visible(self.NO_RECORDS)

    def get_row_data(self, row_index=0):
        """Returns a dict of column header -> cell text for the given row (0-indexed)."""
        headers = self.driver.find_elements(*self.TABLE_HEADERS)
        header_texts = [h.text.strip() for h in headers if h.text.strip()]
        rows = self.driver.find_elements(*self.TABLE_ROWS)
        if row_index >= len(rows):
            self.logger.warning(f"Row index {row_index} out of range ({len(rows)} rows)")
            return {}
        cells = rows[row_index].find_elements(By.TAG_NAME, "td")
        data = {}
        for i, header in enumerate(header_texts):
            if i < len(cells):
                data[header] = cells[i].text.strip()
        self.logger.info(f"Row {row_index} data: {data}")
        return data

    def get_sme_status_from_table(self, identifier):
        """Gets the status badge text for an SME identified by email/name in the table."""
        status_xpath = (
            By.XPATH,
            f"//td[contains(text(), '{identifier}')]/ancestor::tr//span[contains(@class, 'badge')]"
        )
        try:
            return self.get_element_text(status_xpath).strip()
        except Exception:
            self.logger.warning(f"Could not get status for '{identifier}'")
            return "Unknown"

    def click_table_header(self, header_text):
        """Clicks a table header for sorting."""
        header_xpath = (By.XPATH, f"//th[contains(text(), '{header_text}')]")
        self.do_click(header_xpath)
        time.sleep(1)

    def navigate_next_page(self):
        """Clicks next page in pagination."""
        self.do_click(self.PAGINATION_NEXT)
        time.sleep(2)

    def navigate_prev_page(self):
        """Clicks previous page in pagination."""
        self.do_click(self.PAGINATION_PREV)
        time.sleep(2)

    # ═══════════════════════════════════════════════════════════════════════
    # ROW ACTIONS (View, Edit, Activate, Suspend, Auto-Login, Delete)
    # ═══════════════════════════════════════════════════════════════════════
    def _click_row_action(self, xpath_template, identifier):
        """Helper to click an action icon for a specific SME."""
        locator = (By.XPATH, xpath_template.format(identifier=identifier))
        self.do_click(locator)
        time.sleep(2)

    def click_view(self, identifier):
        """Opens the profile/view page of an SME."""
        self.logger.info(f"Clicking View for SME '{identifier}'...")
        self._click_row_action(self.VIEW_ICON_XPATH, identifier)

    def click_edit(self, identifier):
        """Opens the edit form for an SME."""
        self.logger.info(f"Clicking Edit for SME '{identifier}'...")
        self._click_row_action(self.EDIT_ICON_XPATH, identifier)

    def click_activate(self, identifier):
        """Activates a draft/suspended SME and confirms the modal."""
        self.logger.info(f"Activating SME '{identifier}'...")
        self._click_row_action(self.ACTIVATE_ICON_XPATH, identifier)
        self._confirm_action()

    def click_suspend(self, identifier):
        """Suspends an active SME and confirms the modal."""
        self.logger.info(f"Suspending SME '{identifier}'...")
        self._click_row_action(self.SUSPEND_ICON_XPATH, identifier)
        self._confirm_action()

    def click_delete(self, identifier):
        """Deletes an SME and confirms the modal."""
        self.logger.info(f"Deleting SME '{identifier}'...")
        self._click_row_action(self.DELETE_ICON_XPATH, identifier)
        self._confirm_action()

    def expert_auto_login(self, identifier):
        """Finds the expert in the summary table and clicks the auto-login icon."""
        self.logger.info(f"Performing auto-login for SME '{identifier}'...")
        self.search_sme(identifier)
        self._click_row_action(self.AUTO_LOGIN_ICON_XPATH, identifier)
        time.sleep(3)  # Wait for session switch

    def _confirm_action(self):
        """Clicks 'Yes/Confirm' on SweetAlert or modal confirmation dialog."""
        try:
            self.do_click(self.CONFIRM_YES_BTN)
            time.sleep(2)
        except Exception as e:
            self.logger.warning(f"No confirmation dialog appeared: {e}")

    # ═══════════════════════════════════════════════════════════════════════
    # PROFILE VIEW
    # ═══════════════════════════════════════════════════════════════════════
    def get_profile_name(self):
        """Returns the name displayed on the SME profile/detail page."""
        return self.get_element_text(self.PROFILE_NAME)

    def get_profile_status(self):
        """Returns the status badge on the profile page."""
        return self.get_element_text(self.PROFILE_STATUS_BADGE)

    def get_profile_subjects(self):
        """Returns the list of mapped subjects from the profile."""
        try:
            elements = self.driver.find_elements(*self.PROFILE_SUBJECTS)
            return [el.text.strip() for el in elements if el.text.strip()]
        except Exception:
            return []

    def get_profile_schools(self):
        """Returns the list of mapped schools from the profile."""
        try:
            elements = self.driver.find_elements(*self.PROFILE_SCHOOL_LIST)
            return [el.text.strip() for el in elements if el.text.strip()]
        except Exception:
            return []

    def click_back_to_list(self):
        """Navigates back to the summary list from a detail/edit view."""
        self.do_click(self.BACK_TO_LIST_BTN)
        time.sleep(2)

    # ═══════════════════════════════════════════════════════════════════════
    # EDIT PROFILE
    # ═══════════════════════════════════════════════════════════════════════
    def edit_sme_field(self, field_name, new_value):
        """Edits a specific field on the SME edit form by name attribute."""
        field_locator = (By.NAME, field_name)
        self.do_send_keys(field_locator, new_value)

    def save_edit(self):
        """Clicks Save/Update on the edit form."""
        self.do_click(self.EDIT_SAVE_BTN)
        time.sleep(2)

    # ═══════════════════════════════════════════════════════════════════════
    # SCHOOL / SUBJECT MAPPING
    # ═══════════════════════════════════════════════════════════════════════
    def map_school(self, school_name):
        """Maps a school to the SME from their profile."""
        self.logger.info(f"Mapping school '{school_name}' to SME...")
        self.do_click(self.MAP_SCHOOL_BTN)
        time.sleep(1)
        self.select_chosen_option(self.SCHOOL_MAPPING_DROPDOWN, school_name)
        self.do_click(self.SAVE_MAPPING_BTN)
        time.sleep(2)

    def map_subject(self, subject_name):
        """Maps a subject to the SME from their profile."""
        self.logger.info(f"Mapping subject '{subject_name}' to SME...")
        self.do_click(self.MAP_SUBJECT_BTN)
        time.sleep(1)
        self.select_chosen_option(self.SUBJECT_MAPPING_DROPDOWN, subject_name)
        self.do_click(self.SAVE_MAPPING_BTN)
        time.sleep(2)

    def unlink_school(self, school_name):
        """Removes a mapped school from the SME."""
        self.logger.info(f"Unlinking school '{school_name}' from SME...")
        locator = (By.XPATH, self.UNLINK_SCHOOL_XPATH.format(school_name=school_name))
        self.do_click(locator)
        self._confirm_action()

    def select_all_schools(self):
        """Clicks the 'Select All' checkbox in the school mapping list."""
        self.do_click(self.SELECT_ALL_SCHOOLS)
        time.sleep(0.5)

    # ═══════════════════════════════════════════════════════════════════════
    # STATS / DASHBOARD COUNTERS
    # ═══════════════════════════════════════════════════════════════════════
    def get_total_sme_count(self):
        """Returns the total SME count from the dashboard/stats panel."""
        try:
            return int(self.get_element_text(self.TOTAL_SME_COUNT))
        except Exception:
            return -1

    def get_active_sme_count(self):
        """Returns the active SME count from the dashboard/stats panel."""
        try:
            return int(self.get_element_text(self.ACTIVE_SME_COUNT))
        except Exception:
            return -1

    def get_draft_sme_count(self):
        """Returns the draft SME count from the dashboard/stats panel."""
        try:
            return int(self.get_element_text(self.DRAFT_SME_COUNT))
        except Exception:
            return -1

    # ═══════════════════════════════════════════════════════════════════════
    # VALIDATION HELPERS
    # ═══════════════════════════════════════════════════════════════════════
    def is_success_alert_visible(self):
        """Returns True if a success alert/toast is displayed."""
        return self.is_visible(self.SUCCESS_ALERT)

    def is_error_alert_visible(self):
        """Returns True if an error alert/toast is displayed."""
        return self.is_visible(self.ERROR_ALERT)

    def get_validation_errors(self):
        """Returns a list of validation error messages on the page."""
        try:
            errors = self.driver.find_elements(*self.VALIDATION_ERROR)
            return [e.text.strip() for e in errors if e.text.strip()]
        except Exception:
            return []

    def get_page_alert_text(self):
        """Returns the text of the first visible alert (success or error)."""
        for alert_loc in [self.SUCCESS_ALERT, self.ERROR_ALERT]:
            try:
                return self.get_element_text(alert_loc)
            except Exception:
                continue
        return ""

    def check_mandatory_asterisk(self, label_text):
        """Returns True if the label has a red asterisk (*) indicating mandatory field."""
        try:
            label = self.driver.find_element(
                By.XPATH,
                f"//label[contains(normalize-space(text()), '{label_text}')]"
            )
            # Check for asterisk in text or CSS ::after pseudo-element
            has_asterisk = "*" in label.text
            if not has_asterisk:
                # Check for CSS pseudo-element
                after_content = self.driver.execute_script(
                    "return window.getComputedStyle(arguments[0], '::after').getPropertyValue('content');",
                    label
                )
                has_asterisk = "*" in str(after_content) if after_content else False
            return has_asterisk
        except Exception:
            return False

    def is_field_readonly(self, field_name):
        """Checks if a form field is readonly or disabled."""
        try:
            field = self.driver.find_element(By.NAME, field_name)
            return field.get_attribute("readonly") is not None or field.get_attribute("disabled") is not None
        except Exception:
            return False

    # ═══════════════════════════════════════════════════════════════════════
    # SECURITY CHECKS
    # ═══════════════════════════════════════════════════════════════════════
    def is_redirected_to_login(self):
        """Checks if the current URL contains 'login', indicating access denial."""
        return "login" in self.driver.current_url.lower()

    def get_current_url(self):
        """Returns the current browser URL."""
        return self.driver.current_url
