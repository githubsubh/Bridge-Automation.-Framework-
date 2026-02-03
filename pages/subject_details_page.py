from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class SubjectDetailsPage(BasePage):
    # Locators for 7 subjects - assuming they are dropdowns or checkboxes
    # Restoring as generic method to select medium for all
    
    CONTINUE_BTN = (By.ID, "btn_continue_subject")

    def select_medium_for_subject(self, subject_index, medium):
        # Locator might be like named "subject_1_medium"
        locator = (By.ID, f"subject_{subject_index}_medium")
        self.do_send_keys(locator, medium)
        
    def select_all_mediums(self, medium="English"):
        # Select for all 7
        for i in range(1, 8):
            self.select_medium_for_subject(i, medium)

    def click_continue(self):
        self.do_click(self.CONTINUE_BTN)
