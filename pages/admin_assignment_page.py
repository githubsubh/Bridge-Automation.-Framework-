"""
Admin Assignment Page — Page Object for Master >> Assignment module.
====================================================================
Handles navigation to the Assignment section under Masters menu,
creation of new assignments, filling details, file upload, and
submission with validation.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utilities.wait_utils import WaitUtils
import time
import os


class AdminAssignmentPage(BasePage):
    """Page Object for Admin Portal → Master >> Assignment operations."""

    # ── Sidebar / Navigation ──
    MASTERS_MENU = (By.XPATH, "//a[contains(.,'Masters') or contains(.,'Master')]")
    ASSIGNMENT_SUBMENU = (By.XPATH,
        "//ul[contains(@class,'submenu') or contains(@class,'treeview-menu') or contains(@class,'menu-open') or contains(@style,'block')]//a[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'assignment')]"
        " | //a[contains(@href, 'assignment') and not(contains(@href, 'evaluation')) and not(contains(@href, 'allocation'))]"
        " | //a[normalize-space(text())='Assignments' or normalize-space(text())='Assignment']"
    )
    CREATE_NEW_BTN = (By.XPATH,
        "//a[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'add assignment') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'create new') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'add new')]"
        " | //button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'add assignment') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'create new')]"
    )

    # ── Assignment Form Fields (AJAX Modal) ──
    ACADEMIC_YEAR_DROPDOWN = (By.XPATH, "//div[contains(@class, 'modal-content')]//select[contains(@name, 'academic') or contains(@id, 'academic')] | //div[contains(@class, 'modal-content')]//div[contains(@id, 'academic') and contains(@id, 'chosen')]")
    SUBJECT_DROPDOWN = (By.XPATH, "//div[contains(@class, 'modal-content')]//select[contains(@name, 'subject') or contains(@id, 'subject')] | //div[contains(@class, 'modal-content')]//div[contains(@id, 'subject') and contains(@id, 'chosen')]")
    WEIGHTAGE_MARKS_INPUT = (By.XPATH, "//div[contains(@class, 'modal-content')]//input[contains(@placeholder, 'Weightage') or contains(@name, 'weightage') or contains(@id, 'weightage')]")
    MAX_MARKS_INPUT = (By.XPATH, "//div[contains(@class, 'modal-content')]//input[contains(@placeholder, 'Max Marks') or contains(@name, 'max_marks') or contains(@id, 'max_marks')]")
    NO_OF_QUESTIONS_INPUT = (By.XPATH, "//div[contains(@class, 'modal-content')]//input[contains(@placeholder, 'e.g.') or contains(@name, 'question') or contains(@id, 'question')]")
    SUBMIT_BUTTON = (By.XPATH, "//div[contains(@class, 'modal-content')]//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'save') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'submit') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'create') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'add')]")
    
    # ── Status / Feedback ──
    SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert-success")
    ERROR_ALERT = (By.CSS_SELECTOR, ".alert-danger, .alert-error")
    VALIDATION_ERRORS = (By.CSS_SELECTOR, ".help-block, .invalid-feedback, .field-error")
    ASSIGNMENT_TABLE = (By.CSS_SELECTOR, "table.table")
    ASSIGNMENT_ROWS = (By.CSS_SELECTOR, "table.table tbody tr")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WaitUtils(self.driver)

    # ── Navigation ──
    def navigate_to_assignment_section(self):
        """Navigate to Master >> Assignment section in the admin sidebar."""
        self.logger.info("Navigating to Master >> Assignment...")
        self.do_click(self.MASTERS_MENU)
        time.sleep(1)
        self.do_click(self.ASSIGNMENT_SUBMENU)
        time.sleep(2)
        self.logger.info(f"Navigated to Assignment section. URL: {self.driver.current_url}")

    def get_medium_accordion(self, medium):
        return (By.XPATH, f"//div[contains(@class, 'modal-content')]//*[normalize-space(text())='{medium}' or contains(text(), '{medium}')]")

    def get_medium_file_input(self, medium):
        # Find the file input that is inside the same container as the expanded medium
        return (By.XPATH, f"(//div[contains(@class, 'modal-content')]//input[@type='file'])[1]")

    def click_create_new(self):
        """Clicks the 'Create New' / 'Add Assignment' button to open the AJAX modal."""
        self.logger.info("Clicking Create New Assignment button to open modal...")
        self.do_click(self.CREATE_NEW_BTN)
        time.sleep(3) # Wait for AJAX modal to open

    # ── Form Population ──
    def fill_assignment_details(self, subject, academic_year="2025-26", weightage_marks="20", max_marks="100", no_of_questions="5", **kwargs):
        """Fills the assignment creation modal with the provided data."""
        self.logger.info(f"Filling assignment details for Subject: {subject}...")
        
        if academic_year:
            self._select_dropdown(self.ACADEMIC_YEAR_DROPDOWN, academic_year)
        
        if subject:
            self._select_dropdown(self.SUBJECT_DROPDOWN, subject)
            
        self.do_send_keys(self.WEIGHTAGE_MARKS_INPUT, str(weightage_marks))
        self.do_send_keys(self.MAX_MARKS_INPUT, str(max_marks))
        
        # Type the number of questions to trigger the dynamic generation of mark fields
        self.do_send_keys(self.NO_OF_QUESTIONS_INPUT, str(no_of_questions))
        time.sleep(2)  # Wait for JS to generate the fields
        
        # Fill in the marks for each generated question so they sum to max_marks
        marks_per_q = int(max_marks) // int(no_of_questions)
        try:
            for i in range(1, int(no_of_questions) + 1):
                # We try to find the input for Question {i}
                # It might have a label "Question 1", or placeholder "Question 1", or just be the i-th generic input in that row
                xpath = f"(//div[contains(@class, 'modal-content')]//input[not(@type='file') and not(contains(@name, 'weightage')) and not(contains(@name, 'max_marks')) and not(contains(@placeholder, 'e.g.')) and not(contains(@placeholder, 'Weightage')) and not(contains(@placeholder, 'Max'))])[{i}]"
                q_inputs = self.driver.find_elements(By.XPATH, xpath)
                if q_inputs:
                    for inp in q_inputs:
                        if inp.is_displayed():
                            inp.clear()
                            inp.send_keys(str(marks_per_q))
                            break
        except Exception as e:
            self.logger.warning(f"Could not fill individual question marks dynamically: {e}")
        
        self.logger.info("Assignment form fields filled successfully.")
        
    def upload_assignment_file(self, file_path, medium="English"):
        """Uploads a file to the assignment form inside the medium accordion.
        Args:
            file_path: Absolute path to the file to upload.
            medium: The medium name to upload the file for (e.g. English, Assamesse)
        """
        abs_path = os.path.abspath(file_path)
        self.logger.info(f"Uploading assignment file for medium {medium}: {abs_path}")
        if not os.path.exists(abs_path):
            self.logger.error(f"File not found: {abs_path}")
            raise FileNotFoundError(f"Assignment file not found: {abs_path}")

        try:
            self.do_click(self.get_medium_accordion(medium))
            time.sleep(1)
        except Exception as e:
            self.logger.warning(f"Could not click accordion for {medium}: {e}, trying to upload anyway...")

        try:
            file_input = self.driver.find_element(*self.get_medium_file_input(medium))
            file_input.send_keys(abs_path)
            time.sleep(2)
            self.logger.info("File upload completed.")
        except Exception as e:
            self.logger.error(f"Failed to upload file for {medium}: {e}")

    def publish_assignment(self):
        """Clicks the Save/Submit button."""
        self.logger.info("Publishing/Saving assignment...")
        self.do_click(self.SUBMIT_BUTTON)
        time.sleep(2)

    # ── Validation ──
    def is_creation_successful(self):
        """Returns True if a success alert appears after creation."""
        result = self.is_visible(self.SUCCESS_ALERT)
        if result:
            try:
                msg = self.get_element_text(self.SUCCESS_ALERT)
                self.logger.info(f"Assignment creation SUCCESS: {msg}")
            except Exception:
                self.logger.info("Assignment creation SUCCESS (alert visible).")
        else:
            self.logger.error("Assignment creation FAILED — no success alert.")
            self._log_validation_errors()
        return result

    def get_error_message(self):
        """Returns the text of any visible error alert."""
        try:
            if self.is_visible(self.ERROR_ALERT):
                return self.get_element_text(self.ERROR_ALERT)
        except Exception:
            pass
        return None

    def get_assignment_count(self):
        """Returns the number of assignments in the listing table."""
        try:
            rows = self.driver.find_elements(*self.ASSIGNMENT_ROWS)
            count = len(rows)
            self.logger.info(f"Assignments in table: {count}")
            return count
        except Exception:
            self.logger.warning("Could not count assignments in table.")
            return 0

    def verify_assignment_in_list(self, title_text):
        """Checks if a specific assignment title (or subject) appears in the listing table."""
        self.logger.info(f"Searching for assignment '{title_text}' in table...")
        try:
            row_xpath = (By.XPATH, f"//td[contains(text(),'{title_text}')]")
            return self.is_visible(row_xpath)
        except Exception:
            return False

    # ── Private Helpers ──
    def _select_dropdown(self, locator, option_text):
        """Attempts dropdown selection using Chosen.js helper or direct Select."""
        try:
            element = self.driver.find_element(*locator)
            tag = element.tag_name.lower()

            if tag == "select":
                self.select_chosen_option(locator, option_text)
            elif "chosen" in (element.get_attribute("id") or ""):
                self.select_chosen_option(locator, option_text)
            else:
                # Fallback: try clicking and selecting from list
                self.do_click(locator)
                time.sleep(1)
                option_xpath = (By.XPATH,
                    f"//li[contains(text(),'{option_text}')] "
                    f"| //option[contains(text(),'{option_text}')]"
                )
                self.do_click(option_xpath)
        except Exception as e:
            self.logger.warning(f"Dropdown selection failed for '{option_text}': {e}")

    def _set_date_field(self, locator, date_value):
        """Sets a date field using JS to bypass date picker restrictions."""
        try:
            element = self.driver.find_element(*locator)
            self.driver.execute_script(
                "arguments[0].value = arguments[1]; "
                "arguments[0].dispatchEvent(new Event('change'));",
                element, date_value
            )
            self.logger.info(f"Date set to: {date_value}")
        except Exception as e:
            self.logger.warning(f"JS date set failed, trying send_keys: {e}")
            self.do_send_keys(locator, date_value)

    def _log_validation_errors(self):
        """Logs any visible validation error messages on the form."""
        try:
            errors = self.driver.find_elements(*self.VALIDATION_ERRORS)
            for err in errors:
                if err.text.strip():
                    self.logger.error(f"  Validation Error: {err.text.strip()}")
        except Exception:
            pass
