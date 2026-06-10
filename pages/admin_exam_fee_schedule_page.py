from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time

class AdminExamFeeSchedulePage(BasePage):
    # Locators (Based on common NIOS Bridge patterns)
    MASTERS_MENU = (By.XPATH, "//a[contains(.,'Masters')]")
    EXAM_FEE_SCHEDULE_SUBMENU = (By.XPATH, "//a[contains(.,'Exam Fee Schedule')]")
    
    # Date Fields
    START_DATE_FIELD = (By.ID, "examschedule-start_date")
    END_DATE_FIELD = (By.ID, "examschedule-end_date")
    EXTENDED_DATE_FIELD = (By.ID, "examschedule-extended_date")
    LAST_PAYMENT_DATE_FIELD = (By.ID, "examschedule-last_payment_date")
    
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(text(), 'Submit') or contains(text(), 'Save')]")
    SUCCESS_MSG = (By.CSS_SELECTOR, ".alert-success")

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_exam_fee_schedule(self):
        self.logger.info("Navigating to Exam Fee Schedule...")
        self.do_click(self.MASTERS_MENU)
        time.sleep(0.5)
        self.do_click(self.EXAM_FEE_SCHEDULE_SUBMENU)
        time.sleep(1)

    def set_exam_dates(self, start_date, end_date, extended_date, last_payment_date):
        self.logger.info(f"Setting Exam Dates: Start={start_date}, End={end_date}, Ext={extended_date}, LastPay={last_payment_date}")
        
        # Using JS to set dates is often safer for date pickers
        self.driver.execute_script(f"document.getElementById('examschedule-start_date').value='{start_date}'")
        self.driver.execute_script(f"document.getElementById('examschedule-end_date').value='{end_date}'")
        self.driver.execute_script(f"document.getElementById('examschedule-extended_date').value='{extended_date}'")
        self.driver.execute_script(f"document.getElementById('examschedule-last_payment_date').value='{last_payment_date}'")
        
        # Trigger change events
        for field_id in ['examschedule-start_date', 'examschedule-end_date', 'examschedule-extended_date', 'examschedule-last_payment_date']:
            self.driver.execute_script(f"document.getElementById('{field_id}').dispatchEvent(new Event('change'))")
        
        time.sleep(1)
        self.do_click(self.SUBMIT_BUTTON)
        time.sleep(2)

    def is_update_successful(self):
        return self.is_visible(self.SUCCESS_MSG)
