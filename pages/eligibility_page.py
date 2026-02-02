from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class EligibilityPage(BasePage):
    # Locators
    textbox_date_of_appointment_id = (By.ID, "eligibilitydetailform-date_of_appointment")
    # Using a generic submit button locator, can be refined if ID is known
    button_continue_xpath = (By.XPATH, "//button[@type='submit' or contains(text(), 'Continue') or contains(text(), 'Submit')]")

    def __init__(self, driver):
        super().__init__(driver)

    def set_date_of_appointment(self, date):
        """
        Sets the date of appointment using JavaScript to avoid input mask issues.
        Date format should be dd-mm-yyyy.
        """
        element = self.driver.find_element(*self.textbox_date_of_appointment_id)
        self.driver.execute_script("arguments[0].value = arguments[1];", element, date)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", element)
        self.logger.info(f"Set Date of Appointment to '{date}' using JavaScript")

    def click_continue(self):
        try:
            self.do_click(self.button_continue_xpath)
            self.logger.info("Clicked Continue on Eligibility Details page")
        except Exception as e:
            self.logger.warning(f"Standard click failed ({type(e).__name__}), trying JS: {e}")
            element = self.driver.find_element(*self.button_continue_xpath)
            self.driver.execute_script("arguments[0].click();", element)
            self.logger.info("Clicked Continue on Eligibility Details page using JS")
