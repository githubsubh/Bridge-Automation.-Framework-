from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utilities.wait_utils import WaitUtils
import time
import os

class StudentAssignmentPage(BasePage):
    # Sidebar / Dashboard
    MY_ASSIGNMENTS_LINK = (By.XPATH, "//a[contains(.,'My Assignments')]")
    RESULTS_LINK = (By.XPATH, "//a[contains(.,'My Results')]")
    
    # Submission Form
    SUBJECT_SELECT = (By.ID, "subject_select_chosen")
    FILE_INPUT = (By.XPATH, "//input[@type='file']")
    SUBMIT_BTN = (By.XPATH, "//button[contains(text(), 'Submit') or contains(text(), 'Upload')]")
    
    # Download
    DOWNLOAD_BTN_XPATH = "//td[contains(text(),'{subject}')]/following-sibling::td//a[contains(@href, 'download') or contains(text(), 'Download') or @title='Download Assignment']"
    
    # Re-upload / Action buttons
    REUPLOAD_BTN_XPATH = "//td[contains(text(),'{subject}')]/following-sibling::td//a[contains(@href, 'upload') or contains(text(), 'Re-upload') or @title='Re-upload']"
    
    # Status Table
    ASSIGNMENT_ROWS = (By.CSS_SELECTOR, "table.assignment-status-table tr, table.table tr")
    SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert-success")
    ERROR_ALERT = (By.CSS_SELECTOR, ".alert-danger, .alert-error")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WaitUtils(self.driver)

    def navigate_to_my_assignments(self):
        self.do_click(self.MY_ASSIGNMENTS_LINK)
        time.sleep(2)

    def download_assignment(self, subject_name):
        """Downloads the assignment file for a given subject."""
        self.logger.info(f"Downloading assignment for {subject_name}...")
        download_xpath = (By.XPATH, self.DOWNLOAD_BTN_XPATH.format(subject=subject_name))
        if self.is_visible(download_xpath):
            self.do_click(download_xpath)
            time.sleep(3) # Wait for download
            return True
        else:
            self.logger.warning(f"Download button not found for {subject_name}")
            return False

    def is_upload_allowed(self, subject_name):
        """Checks if upload/re-upload is allowed (before deadline)."""
        reupload_xpath = (By.XPATH, self.REUPLOAD_BTN_XPATH.format(subject=subject_name))
        return self.is_visible(reupload_xpath)

    def click_upload_action(self, subject_name):
        """Clicks the upload/re-upload button in the grid for the subject."""
        reupload_xpath = (By.XPATH, self.REUPLOAD_BTN_XPATH.format(subject=subject_name))
        self.do_click(reupload_xpath)
        time.sleep(1)

    def submit_assignment(self, subject_name, file_path, direct_upload=False):
        """Uploads and submits the assignment."""
        self.logger.info(f"Submitting assignment for {subject_name}...")
        if not direct_upload:
            self.select_chosen_option(self.SUBJECT_SELECT, subject_name)
            
        abs_path = os.path.abspath(file_path)
        self.do_send_keys(self.FILE_INPUT, abs_path)
        time.sleep(1)
        self.do_click(self.SUBMIT_BTN)
        time.sleep(2)

    def is_submission_successful(self):
        return self.is_visible(self.SUCCESS_ALERT)

    def get_error_message(self):
        if self.is_visible(self.ERROR_ALERT):
            return self.get_element_text(self.ERROR_ALERT)
        return None

    def get_assignment_marks(self, subject_name: str) -> str:
        """Return the marks displayed for a given subject in the status table."""
        marks_xpath = (
            By.XPATH,
            f"//td[contains(text(),'{subject_name}')]/following-sibling::td[@class='marks' or position()=4]"
        )
        try:
            return self.get_element_text(marks_xpath).strip()
        except:
            return ""

    def verify_result_published(self, subject_name):
        self.do_click(self.RESULTS_LINK)
        time.sleep(1)
        result_xpath = (By.XPATH, f"//td[contains(text(), '{subject_name}')]/following-sibling::td[contains(@class, 'result')]")
        return self.is_visible(result_xpath)

    def get_assignment_status(self, subject_name: str) -> str:
        """Return the status text for a given subject in the assignment table."""
        status_xpath = (
            By.XPATH,
            f"//td[contains(text(),'{subject_name}')]/following-sibling::td[@class='status' or contains(@class, 'badge') or position()=3]"
        )
        try:
            return self.get_element_text(status_xpath).strip()
        except:
            return ""
