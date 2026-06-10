"""
Result / Rechecking / Revaluation Page — Page Object.
=====================================================
Handles:
  - Viewing published results
  - Applying for rechecking
  - Applying for revaluation
  - Validating request submissions
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utilities.wait_utils import WaitUtils
import time


class ResultPage(BasePage):
    """Page Object for Student Result, Rechecking, and Revaluation modules."""

    # ── Navigation (from Dashboard) ──
    RESULTS_CARD = (By.XPATH,
        "//*[self::h5 or self::h6][normalize-space(.)='Results' "
        "or normalize-space(.)='My Results' or normalize-space(.)='Result']"
    )
    RESULTS_LINK = (By.XPATH,
        "//a[contains(@href,'result') or contains(text(),'View Result') "
        "or contains(text(),'Public Exam Results') or contains(text(),'Check Result')]"
    )
    RECHECKING_LINK = (By.XPATH,
        "//a[contains(@href,'rechecking') or contains(text(),'Rechecking') "
        "or contains(text(),'Apply for Rechecking')]"
    )
    REVALUATION_LINK = (By.XPATH,
        "//a[contains(@href,'revaluation') or contains(text(),'Revaluation') "
        "or contains(text(),'Apply for Revaluation')]"
    )

    # ── Results Table ──
    RESULTS_TABLE = (By.CSS_SELECTOR, "table.table, table.result-table")
    RESULTS_TABLE_ROWS = (By.CSS_SELECTOR,
        "table.table tbody tr, table.result-table tbody tr"
    )
    SUBJECT_COL_XPATH = "//td[contains(text(),'{subject}')]"

    # ── Result Details ──
    RESULT_STATUS_BADGE = (By.CSS_SELECTOR, ".badge, .status-badge")
    MARKS_OBTAINED_XPATH = (
        "//td[contains(text(),'{subject}')]/following-sibling::td[contains(@class,'marks') "
        "or position()=2]"
    )
    TOTAL_MARKS_XPATH = (
        "//td[contains(text(),'{subject}')]/following-sibling::td[position()=3]"
    )
    GRADE_XPATH = (
        "//td[contains(text(),'{subject}')]/following-sibling::td[contains(@class,'grade') "
        "or position()=4]"
    )
    OVERALL_RESULT = (By.XPATH,
        "//div[contains(@class,'result-status') or contains(@class,'overall')]"
        " | //*[contains(text(),'Pass') or contains(text(),'Fail')]"
    )

    # ── Rechecking Form ──
    RECHECKING_SUBJECT_CHECKBOX = (By.XPATH,
        "//input[@type='checkbox' and contains(@name,'rechecking')]"
    )
    RECHECKING_SUBJECT_SELECT = (By.XPATH,
        "//select[@name='rechecking_subject' or contains(@id,'rechecking')]"
        " | //div[contains(@id,'rechecking_subject_chosen')]"
    )
    RECHECKING_REASON_TEXTAREA = (By.XPATH,
        "//textarea[@name='reason' or @name='rechecking_reason' "
        "or @placeholder='Enter Reason']"
    )
    RECHECKING_SUBMIT_BTN = (By.XPATH,
        "//button[contains(text(),'Submit') or contains(text(),'Apply for Rechecking')]"
    )

    # ── Revaluation Form ──
    REVALUATION_SUBJECT_CHECKBOX = (By.XPATH,
        "//input[@type='checkbox' and contains(@name,'revaluation')]"
    )
    REVALUATION_SUBJECT_SELECT = (By.XPATH,
        "//select[@name='revaluation_subject' or contains(@id,'revaluation')]"
        " | //div[contains(@id,'revaluation_subject_chosen')]"
    )
    REVALUATION_REASON_TEXTAREA = (By.XPATH,
        "//textarea[@name='reason' or @name='revaluation_reason']"
    )
    REVALUATION_SUBMIT_BTN = (By.XPATH,
        "//button[contains(text(),'Submit') or contains(text(),'Apply for Revaluation')]"
    )

    # ── Payment (if required for rechecking/revaluation) ──
    PAYMENT_PROCEED_BTN = (By.XPATH,
        "//button[contains(text(),'Proceed to Payment') "
        "or contains(text(),'Pay Now')]"
    )

    # ── Status / Feedback ──
    SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert-success")
    ERROR_ALERT = (By.CSS_SELECTOR, ".alert-danger, .alert-error")
    INFO_ALERT = (By.CSS_SELECTOR, ".alert-info, .alert-warning")
    NO_RESULT_MSG = (By.XPATH,
        "//*[contains(text(),'No result') or contains(text(),'not available') "
        "or contains(text(),'Result not published')]"
    )

    # ── Request History Table ──
    REQUEST_HISTORY_TABLE = (By.CSS_SELECTOR,
        "table.request-history, table.table"
    )
    REQUEST_ROWS = (By.CSS_SELECTOR,
        "table.request-history tbody tr, table.table tbody tr"
    )

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WaitUtils(self.driver)

    # ── Navigation ──
    def navigate_to_results(self):
        """Navigate to the Results section from the dashboard."""
        self.logger.info("Navigating to Results section...")
        try:
            self.do_click(self.RESULTS_LINK)
        except Exception:
            self.logger.info("Results link not found in nav. Trying card click...")
            try:
                self.do_click(self.RESULTS_CARD)
                time.sleep(1)
                self.do_click(self.RESULTS_LINK)
            except Exception:
                self.driver.get("https://bridge-uat.nios.ac.in/results")
        time.sleep(2)
        self.logger.info(f"On Results page. URL: {self.driver.current_url}")

    def navigate_to_rechecking(self):
        """Navigate to the Rechecking application page."""
        self.logger.info("Navigating to Rechecking section...")
        try:
            self.do_click(self.RECHECKING_LINK)
        except Exception:
            self.driver.get("https://bridge-uat.nios.ac.in/results/rechecking")
        time.sleep(2)

    def navigate_to_revaluation(self):
        """Navigate to the Revaluation application page."""
        self.logger.info("Navigating to Revaluation section...")
        try:
            self.do_click(self.REVALUATION_LINK)
        except Exception:
            self.driver.get("https://bridge-uat.nios.ac.in/results/revaluation")
        time.sleep(2)

    # ── Result Viewing ──
    def is_result_available(self):
        """Checks if results are published and available.

        Returns:
            True if result table is visible, False if 'not available' message shown.
        """
        self.logger.info("Checking if results are available...")
        if self.is_visible(self.NO_RESULT_MSG):
            self.logger.info("Results not yet published.")
            return False
        if self.is_visible(self.RESULTS_TABLE):
            self.logger.info("Results table is visible.")
            return True
        self.logger.warning("Could not determine result availability.")
        return False

    def get_all_results(self):
        """Extracts all subject results from the results table.

        Returns:
            List of dicts with keys: subject, marks, total, grade, status.
        """
        self.logger.info("Extracting result data from table...")
        results = []
        try:
            rows = self.driver.find_elements(*self.RESULTS_TABLE_ROWS)
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) >= 3:
                    result_entry = {
                        "subject": cols[0].text.strip() if len(cols) > 0 else "",
                        "marks": cols[1].text.strip() if len(cols) > 1 else "",
                        "total": cols[2].text.strip() if len(cols) > 2 else "",
                        "grade": cols[3].text.strip() if len(cols) > 3 else "",
                        "status": cols[4].text.strip() if len(cols) > 4 else "",
                    }
                    results.append(result_entry)
                    self.logger.info(f"  Subject: {result_entry['subject']} | "
                                     f"Marks: {result_entry['marks']} | "
                                     f"Grade: {result_entry['grade']}")
        except Exception as e:
            self.logger.error(f"Failed to extract results: {e}")
        return results

    def get_subject_marks(self, subject_name):
        """Returns the marks obtained for a specific subject.

        Args:
            subject_name: Name of the subject.

        Returns:
            Marks string or None if not found.
        """
        marks_locator = (By.XPATH,
            self.MARKS_OBTAINED_XPATH.format(subject=subject_name))
        try:
            return self.get_element_text(marks_locator).strip()
        except Exception:
            self.logger.warning(f"Could not find marks for '{subject_name}'.")
            return None

    def get_subject_grade(self, subject_name):
        """Returns the grade for a specific subject."""
        grade_locator = (By.XPATH, self.GRADE_XPATH.format(subject=subject_name))
        try:
            return self.get_element_text(grade_locator).strip()
        except Exception:
            return None

    def get_overall_result_status(self):
        """Returns the overall result status (Pass/Fail)."""
        try:
            return self.get_element_text(self.OVERALL_RESULT).strip()
        except Exception:
            return None

    # ── Rechecking Application ──
    def apply_for_rechecking(self, subjects=None, reason="Requesting rechecking of answer sheet"):
        """Applies for rechecking for the specified subjects.

        Args:
            subjects: List of subject names to select for rechecking.
                      If None, selects all available subjects.
            reason: Reason text for the rechecking application.
        """
        self.logger.info(f"Applying for rechecking. Subjects: {subjects or 'ALL'}")

        # Select subjects
        if subjects:
            for subj in subjects:
                self._select_subject_checkbox(subj, "rechecking")
        else:
            # Select all available checkboxes
            checkboxes = self.driver.find_elements(*self.RECHECKING_SUBJECT_CHECKBOX)
            for cb in checkboxes:
                if not cb.is_selected():
                    cb.click()
                    time.sleep(0.3)

        # Enter reason
        try:
            self.do_send_keys(self.RECHECKING_REASON_TEXTAREA, reason)
        except Exception:
            self.logger.info("Reason textarea not required for rechecking.")

        # Submit
        self.do_click(self.RECHECKING_SUBMIT_BTN)
        time.sleep(3)

    # ── Revaluation Application ──
    def apply_for_revaluation(self, subjects=None, reason="Requesting revaluation of answer sheet"):
        """Applies for revaluation for the specified subjects.

        Args:
            subjects: List of subject names to select for revaluation.
            reason: Reason text for the revaluation application.
        """
        self.logger.info(f"Applying for revaluation. Subjects: {subjects or 'ALL'}")

        if subjects:
            for subj in subjects:
                self._select_subject_checkbox(subj, "revaluation")
        else:
            checkboxes = self.driver.find_elements(*self.REVALUATION_SUBJECT_CHECKBOX)
            for cb in checkboxes:
                if not cb.is_selected():
                    cb.click()
                    time.sleep(0.3)

        try:
            self.do_send_keys(self.REVALUATION_REASON_TEXTAREA, reason)
        except Exception:
            self.logger.info("Reason textarea not required for revaluation.")

        self.do_click(self.REVALUATION_SUBMIT_BTN)
        time.sleep(3)

    # ── Payment ──
    def proceed_to_payment(self):
        """Clicks the payment button if rechecking/revaluation requires payment."""
        self.logger.info("Proceeding to payment for rechecking/revaluation...")
        try:
            self.do_click(self.PAYMENT_PROCEED_BTN)
            time.sleep(2)
            return True
        except Exception:
            self.logger.info("No payment step required.")
            return False

    # ── Validation ──
    def is_request_successful(self):
        """Returns True if a success alert appears after submission."""
        result = self.is_visible(self.SUCCESS_ALERT)
        if result:
            try:
                msg = self.get_element_text(self.SUCCESS_ALERT)
                self.logger.info(f"Request submission SUCCESS: {msg}")
            except Exception:
                self.logger.info("Request submission SUCCESS.")
        else:
            self.logger.error("Request submission FAILED.")
        return result

    def get_error_message(self):
        """Returns visible error message text."""
        try:
            if self.is_visible(self.ERROR_ALERT):
                return self.get_element_text(self.ERROR_ALERT)
        except Exception:
            pass
        return None

    def get_info_message(self):
        """Returns visible info/warning message text."""
        try:
            if self.is_visible(self.INFO_ALERT):
                return self.get_element_text(self.INFO_ALERT)
        except Exception:
            pass
        return None

    def get_request_history(self):
        """Extracts the request history (rechecking/revaluation) from the table.

        Returns:
            List of dicts with request details.
        """
        self.logger.info("Extracting request history...")
        requests = []
        try:
            rows = self.driver.find_elements(*self.REQUEST_ROWS)
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) >= 3:
                    req = {
                        "id": cols[0].text.strip() if len(cols) > 0 else "",
                        "type": cols[1].text.strip() if len(cols) > 1 else "",
                        "subject": cols[2].text.strip() if len(cols) > 2 else "",
                        "status": cols[3].text.strip() if len(cols) > 3 else "",
                        "date": cols[4].text.strip() if len(cols) > 4 else "",
                    }
                    requests.append(req)
        except Exception as e:
            self.logger.error(f"Failed to extract request history: {e}")
        return requests

    def verify_request_exists(self, request_type):
        """Checks if a request of the given type exists in the history.

        Args:
            request_type: 'rechecking' or 'revaluation'.

        Returns:
            True if found, False otherwise.
        """
        history = self.get_request_history()
        for req in history:
            if request_type.lower() in req.get("type", "").lower():
                self.logger.info(f"Found {request_type} request: {req}")
                return True
        self.logger.warning(f"No {request_type} request found in history.")
        return False

    # ── Private Helpers ──
    def _select_subject_checkbox(self, subject_name, form_type):
        """Selects a specific subject checkbox by subject name.

        Args:
            subject_name: Subject text to match.
            form_type: 'rechecking' or 'revaluation'.
        """
        try:
            cb_xpath = (By.XPATH,
                f"//td[contains(text(),'{subject_name}')]"
                f"/preceding-sibling::td//input[@type='checkbox']"
                f" | //label[contains(text(),'{subject_name}')]"
                f"/preceding-sibling::input[@type='checkbox']"
                f" | //label[contains(text(),'{subject_name}')]"
                f"//input[@type='checkbox']"
            )
            checkbox = self.driver.find_element(*cb_xpath)
            if not checkbox.is_selected():
                checkbox.click()
                self.logger.info(f"Selected {subject_name} for {form_type}.")
            time.sleep(0.3)
        except Exception as e:
            self.logger.warning(f"Could not select checkbox for '{subject_name}': {e}")
