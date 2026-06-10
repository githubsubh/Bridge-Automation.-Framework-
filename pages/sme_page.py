from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time

class SmePage(BasePage):
    """Page Object for Subject Matter Expert (SME) actions.
    Only the methods required for the end‑to‑end assignment workflow are implemented.
    """

    # Locators – adjust IDs/XPath if UI changes
    MENU_EVALUATION = (By.XPATH, "//a[contains(.,'Assignment Evaluation')]")
    SUBJECT_DROPDOWN = (By.ID, "evaluation-subject_chosen")
    MARKS_INPUT = (By.ID, "evaluation-marks")
    REMARKS_TEXTAREA = (By.ID, "evaluation-remarks")
    SUBMIT_BTN = (By.XPATH, "//button[contains(text(),'Submit Evaluation')]")
    SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert-success")

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_evaluation(self):
        """Navigate to the SME Assignment Evaluation page."""
        self.do_click(self.MENU_EVALUATION)
        time.sleep(2)

    def evaluate_assignment(self, subject_name: str, marks: str, remarks: str) -> None:
        """Select the subject, enter marks and remarks, then submit the evaluation."""
        self.select_chosen_option(self.SUBJECT_DROPDOWN, subject_name)
        self.do_send_keys(self.MARKS_INPUT, marks)
        self.do_send_keys(self.REMARKS_TEXTAREA, remarks)
        self.do_click(self.SUBMIT_BTN)
        time.sleep(2)

    def is_evaluation_successful(self) -> bool:
        """Return True if a success alert appears after submitting evaluation."""
        return self.is_visible(self.SUCCESS_ALERT)
