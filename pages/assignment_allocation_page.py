from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time

class AssignmentAllocationPage(BasePage):
    # Sidebar — confirmed from live inspection (24 Apr 2026)
    # "Assignment Management" is a TOP-LEVEL sidebar item (not under Masters)
    ASSIGNMENT_MGMT_MENU = (By.XPATH, "//a[contains(.,'Assignment Management')]")
    UPLOADED_ASSIGNMENTS_SUBMENU = (By.XPATH, "//a[contains(.,'Uploaded Assignments')]")
    ASSIGN_TO_EXPERT_SUBMENU = (By.XPATH, "//a[contains(.,'Assign to Expert')]")
    ASSIGNMENT_EVAL_SUBMENU = (By.XPATH, "//a[contains(.,'Assignment Evaluation')]")

    # Filter (top-right button on Assign to Expert page)
    FILTER_BUTTON = (By.XPATH, "//button[contains(.,'Filter')] | //a[contains(.,'Filter')]")
    
    # Filters (inside filter panel)
    SCHOOL_DROPDOWN = (By.ID, "school_id_chosen")
    SUBJECT_DROPDOWN = (By.ID, "subject_id_chosen")
    MEDIUM_DROPDOWN = (By.ID, "medium_id_chosen")
    SEARCH_BUTTON = (By.XPATH, "//button[contains(text(), 'Search') or contains(text(), 'Apply')]")
    
    # Allocation Table
    SELECT_ALL_CHECKBOX = (By.ID, "select_all_assignments")
    EXPERT_DROPDOWN = (By.ID, "expert_id_chosen")
    ALLOCATE_BUTTON = (By.XPATH, "//button[contains(text(), 'Allocate Now') or contains(text(), 'Allocate')]")
    
    # Status
    SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert-success")
    NO_RESULTS_MSG = (By.XPATH, "//*[contains(text(),'No results found')]")

    def __init__(self, driver):
        super().__init__(driver)

    def create_and_publish_assignment(
        self,
        title: str,
        description: str,
        subject: str,
        class_name: str,
        section: str,
        due_date: str,
        total_marks: str,
    ) -> None:
        """Fills the admin *Create Assignment* form and publishes it.

        The locators used below correspond to the current NIOS Bridge UI.
        Adjust IDs/XPath if the UI changes.
        """
        # Locators – add to this file if they are not already defined
        TITLE_INPUT = (By.ID, "assignment-title")
        DESC_INPUT = (By.ID, "assignment-description")
        SUBJECT_DROPDOWN = (By.ID, "assignment-subject_chosen")
        CLASS_DROPDOWN = (By.ID, "assignment-class_chosen")
        SECTION_INPUT = (By.ID, "assignment-section")
        DUE_DATE_INPUT = (By.ID, "assignment-due_date")
        TOTAL_MARKS_INPUT = (By.ID, "assignment-total_marks")
        PUBLISH_BTN = (By.XPATH, "//button[contains(text(),'Publish') or contains(@class,'publish')]")
        # Populate form fields
        self.do_send_keys(TITLE_INPUT, title)
        self.do_send_keys(DESC_INPUT, description)
        self.select_chosen_option(SUBJECT_DROPDOWN, subject)
        self.select_chosen_option(CLASS_DROPDOWN, class_name)
        self.do_send_keys(SECTION_INPUT, section)
        self.do_send_keys(DUE_DATE_INPUT, due_date)
        self.do_send_keys(TOTAL_MARKS_INPUT, total_marks)
        # Submit
        self.do_click(PUBLISH_BTN)
        time.sleep(2)

    def is_creation_successful(self) -> bool:
        """Return True if a success alert appears after publishing."""
        SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert-success")
        return self.is_visible(SUCCESS_ALERT)

        super().__init__(driver)

    def navigate_to_allocation(self):
        """Navigate to Assign to Expert page. Assignment Management is a top-level menu."""
        self.do_click(self.ASSIGNMENT_MGMT_MENU)
        time.sleep(1)
        self.do_click(self.ASSIGN_TO_EXPERT_SUBMENU)
        time.sleep(2)

    def navigate_to_uploaded_assignments(self):
        """Navigate to Uploaded Assignments page."""
        self.do_click(self.ASSIGNMENT_MGMT_MENU)
        time.sleep(1)
        self.do_click(self.UPLOADED_ASSIGNMENTS_SUBMENU)
        time.sleep(2)

    def navigate_to_evaluation(self):
        """Navigate to Assignment Evaluation page."""
        self.do_click(self.ASSIGNMENT_MGMT_MENU)
        time.sleep(1)
        self.do_click(self.ASSIGNMENT_EVAL_SUBMENU)
        time.sleep(2)

    def apply_filter(self, school=None, subject=None, medium=None):
        """Click Filter button and apply school/subject/medium filters."""
        self.do_click(self.FILTER_BUTTON)
        time.sleep(1)
        if school:
            self.select_chosen_option(self.SCHOOL_DROPDOWN, school)
        if subject:
            self.select_chosen_option(self.SUBJECT_DROPDOWN, subject)
        if medium:
            self.select_chosen_option(self.MEDIUM_DROPDOWN, medium)
        self.do_click(self.SEARCH_BUTTON)
        time.sleep(2)

    def allocate_assignments(self, school, subject, expert_name):
        self.apply_filter(school=school, subject=subject)
        
        self.do_click(self.SELECT_ALL_CHECKBOX)
        self.select_chosen_option(self.EXPERT_DROPDOWN, expert_name)
        self.do_click(self.ALLOCATE_BUTTON)
        time.sleep(2)

    def is_allocation_successful(self):
        return self.is_visible(self.SUCCESS_ALERT)

    def has_no_results(self):
        return self.is_visible(self.NO_RESULTS_MSG)
