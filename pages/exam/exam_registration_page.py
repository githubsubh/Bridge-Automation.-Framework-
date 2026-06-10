from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utilities.wait_utils import WaitUtils
from constants.exam_constants import ExamConstants

class ExamRegistrationPage(BasePage):
    # --- Locators ---
    # Dashboard Nav
    EXAM_REG_BOX = (By.XPATH, "//*[self::h5 or self::h6][normalize-space(.)='Exam Registration']")
    REGISTER_LINK = (By.XPATH, "//*[self::h5 or self::h6][normalize-space(.)='Exam Registration']/ancestor::div[contains(@class, 'card')]//a[contains(text(), 'Register')]")
    
    # Session Details
    ACADEMIC_YEAR = (By.XPATH, "//div[contains(text(), 'Academic Year')]/following-sibling::div")
    BLOCK = (By.XPATH, "//div[contains(text(), 'Block')]/following-sibling::div")
    REG_OPEN_DATE = (By.XPATH, "//div[contains(text(), 'Registration Open From')]/following-sibling::div")
    LAST_DATE = (By.XPATH, "//div[contains(text(), 'Last Date')]/following-sibling::div")
    
    # Actions
    PROCEED_BTN = (By.XPATH, "//button[contains(text(), 'PROCEED')]")
    ALREADY_REG_MSG = (By.XPATH, "//div[contains(@class, 'alert')]//p[contains(text(), 'already registered')]")
    DYNAMIC_WARNING = (By.XPATH, "//div[contains(@class, 'alert-warning')] | //marquee | //div[contains(@class, 'suggestion')]")
    
    # Subjects Table
    SUBJECTS_TABLE = (By.XPATH, "//table[contains(@class, 'table')]")
    SUBJECTS_TABLE_ROWS = (By.XPATH, "//table[contains(@class, 'table')]/tbody/tr")
    SUBJECT_NAME_COL = 2
    MEDIUM_COL = 3
    EXAM_STATUS_COL = 4

    def __init__(self, driver):
        super().__init__(driver)
        self.wait_utils = WaitUtils(self.driver)

    def navigate_to_exam_registration(self):
        """Navigates from Dashboard to Exam Registration page."""
        self.logger.info("Navigating to Exam Registration via Dashboard...")
        try:
            self.wait_utils.visibility_wait(self.EXAM_REG_BOX)
            self.do_click(self.REGISTER_LINK)
            self.logger.info("Clicked Register link.")
        except Exception as e:
            self.logger.error(f"Navigation failed: {e}. Saving DOM for analysis...")
            with open("dashboard_dom_debug.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            raise

    def validate_active_session(self):
        """Validates the active exam session details on the page."""
        self.logger.info("Validating Active Exam Session details...")
        details = {
            "Academic Year": self.get_element_text(self.ACADEMIC_YEAR),
            "Block": self.get_element_text(self.BLOCK),
            "Open Date": self.get_element_text(self.REG_OPEN_DATE),
            "Last Date": self.get_element_text(self.LAST_DATE)
        }
        for key, val in details.items():
            self.logger.info(f"{key}: {val}")
        return details

    def get_subjects_list(self):
        """Extracts and logs the list of subjects from the table."""
        self.logger.info("Extracting subjects list...")
        rows = self.driver.find_elements(*self.SUBJECTS_TABLE_ROWS)
        subjects = []
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 4:
                subject_info = {
                    "Name": cols[1].text.strip(),
                    "Medium": cols[2].text.strip(),
                    "Status": cols[3].text.strip()
                }
                subjects.append(subject_info)
                self.logger.info(f"Found Subject: {subject_info}")
        return subjects

    def validate_proceed_button(self):
        """Checks if Proceed button is visible and clickable."""
        is_visible = self.is_visible(self.PROCEED_BTN)
        self.logger.info(f"Proceed button visibility: {is_visible}")
        return is_visible

    def click_proceed(self):
        """Clicks the Proceed button to navigate to OTP page."""
        self.logger.info("Clicking PROCEED button...")
        self.wait_utils.clickable_wait(self.PROCEED_BTN).click()

    def check_already_registered(self):
        """Checks if the user is already registered for the current exam session."""
        self.logger.info("Checking if user is already registered...")
        try:
            # Short wait to check for existence of already registered message
            msg_element = self.driver.find_elements(*self.ALREADY_REG_MSG)
            if msg_element and msg_element[0].is_displayed():
                self.logger.warning("User is ALREADY registered for this exam.")
                return True
            return False
        except:
            return False

    def validate_subjects_data(self, subjects_list):
        """
        Validates that subjects have essential data (Name and Status).
        :param subjects_list: List of dicts from get_subjects_list()
        """
        self.logger.info("Validating subject data integrity...")
        if not subjects_list:
            self.logger.error("Empty subjects list provided for validation.")
            return False
            
        for subj in subjects_list:
            if not subj["Name"] or not subj["Status"]:
                self.logger.error(f"Incomplete subject data found: {subj}")
                return False
        
        self.logger.info("All subjects validated successfully.")
        return True

    def get_dynamic_warning(self):
        """Returns the text of any dynamic warning or suggestion displayed."""
        if self.is_visible(self.DYNAMIC_WARNING):
            warning_text = self.get_element_text(self.DYNAMIC_WARNING)
            self.logger.info(f"Dynamic warning found: {warning_text}")
            return warning_text
        return None
