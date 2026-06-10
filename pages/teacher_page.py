from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time

class TeacherPage(BasePage):
    """Page object for Teacher dashboard actions.
    Only the method required for the assignment workflow is implemented.
    """

    # Locator for the "Student View" toggle/button – adjust if UI differs
    STUDENT_VIEW_BTN = (By.XPATH, "//button[contains(.,'Student View') or @title='Student View']")

    def __init__(self, driver):
        super().__init__(driver)

    def switch_to_student_view(self):
        """Click the UI element that toggles the teacher dashboard into student view.
        This method logs the action and waits briefly for the view to load.
        """
        self.logger.info("Switching to Student View from Teacher Dashboard...")
        self.do_click(self.STUDENT_VIEW_BTN)
        time.sleep(2)  # allow page transition
        self.logger.info("Student View activated.")
