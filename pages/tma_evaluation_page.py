from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utilities.wait_utils import WaitUtils
import time

class TMAEvaluationPage(BasePage):
    # Sidebar
    ASSIGNMENT_MGMT_MENU = (By.XPATH, "//a[contains(.,'Assignment Management')]")
    ASSIGNMENT_EVAL_SUBMENU = (By.XPATH, "//a[contains(.,'Assignment Evaluation')]")
    
    # List / Table
    PREVIEW_BUTTON = (By.XPATH, "//button[contains(.,'Preview') or contains(.,'Evaluate')]")
    EVALUATE_ROW_BTN = "//td[contains(text(), '{assignment_id}')]/following-sibling::td//button[contains(.,'Evaluate') or contains(@title, 'Evaluate')]"
    ASSIGNMENT_CONTENT = (By.ID, "tma_preview_content")
    MODAL_CLOSE = (By.CSS_SELECTOR, ".btn-close, .modal-header .close")
    
    # Evaluation Form
    MARKS_INPUT = (By.NAME, "evaluation_marks")
    REMARKS_AREA = (By.NAME, "evaluation_remarks")
    SUBMIT_EVALUATION_BTN = (By.ID, "submit_evaluation_marks")
    STATUS_BADGE = (By.CSS_SELECTOR, ".badge")
    SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert-success")
    
    # Question-wise evaluation
    Q_MARKS_INPUT_XPATH = "//input[contains(@name, 'question_marks') and contains(@name, '[{q_no}]')]"
    Q_REMARKS_INPUT_XPATH = "//input[contains(@name, 'question_remarks') and contains(@name, '[{q_no}]')]"

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WaitUtils(self.driver)

    def navigate_to_evaluation(self):
        """Navigate to Assignment Evaluation page."""
        self.do_click(self.ASSIGNMENT_MGMT_MENU)
        time.sleep(1)
        self.do_click(self.ASSIGNMENT_EVAL_SUBMENU)
        time.sleep(2)

    def click_preview(self):
        self.do_click(self.PREVIEW_BUTTON)
        time.sleep(2)
        
    def click_evaluate_for_assignment(self, assignment_id):
        """Clicks evaluate for a specific assignment ID."""
        btn_xpath = (By.XPATH, self.EVALUATE_ROW_BTN.format(assignment_id=assignment_id))
        self.do_click(btn_xpath)
        time.sleep(2)

    def is_assignment_visible(self):
        """Checks if assignment content (PDF/Images) is loaded."""
        try:
            return self.is_visible(self.ASSIGNMENT_CONTENT)
        except:
            return False

    def enter_question_marks(self, q_no, marks, remarks=""):
        """Enters marks and remarks for a specific question number."""
        self.logger.info(f"Entering marks for Question {q_no}: {marks}")
        marks_locator = (By.XPATH, self.Q_MARKS_INPUT_XPATH.format(q_no=q_no))
        
        if self.is_visible(marks_locator):
            self.do_send_keys(marks_locator, str(marks))
            if remarks:
                remarks_locator = (By.XPATH, self.Q_REMARKS_INPUT_XPATH.format(q_no=q_no))
                if self.is_visible(remarks_locator):
                    self.do_send_keys(remarks_locator, remarks)
        else:
            self.logger.warning(f"Question {q_no} marks input not found. Assuming overall grading only.")

    def submit_marks(self, marks=None, remarks="Evaluated by automation", q_marks_dict=None):
        """Submits evaluation, supporting both overall and question-wise marking."""
        # Handle question-wise marks if provided
        if q_marks_dict:
            for q_no, q_data in q_marks_dict.items():
                self.enter_question_marks(q_no, q_data.get('marks'), q_data.get('remarks', ''))
                
        # Overall marks/remarks
        if marks:
            self.do_send_keys(self.MARKS_INPUT, str(marks))
            
        self.do_send_keys(self.REMARKS_AREA, remarks)
        self.do_click(self.SUBMIT_EVALUATION_BTN)
        time.sleep(2)

    def get_assignment_status(self, assignment_id):
        """Returns the status text of a specific assignment from the list."""
        status_xpath = (By.XPATH, f"//td[contains(text(), '{assignment_id}')]/following-sibling::td//span[contains(@class, 'badge')]")
        try:
            return self.get_element_text(status_xpath).strip()
        except:
            return "Unknown"
            
    def is_evaluation_successful(self):
        """Checks if the evaluation was successfully saved."""
        return self.is_visible(self.SUCCESS_ALERT)
