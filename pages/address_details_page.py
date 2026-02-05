from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class AddressDetailsPage(BasePage):
    # Locators - using exact IDs from HTML inspection
    ADDRESS_LINE_1 = (By.ID, "addressdetailsform-permanent_address1")
    STREET_LOCALITY = (By.ID, "addressdetailsform-permanent_address2")
    STATE_CHOSEN = (By.ID, "state_dropdown_2_chosen")
    DISTRICT_CHOSEN = (By.ID, "district_dropdown_2_chosen")
    PINCODE_INPUT = (By.ID, "addressdetailsform-permanent_pincode")
    
    CONTINUE_BTN = (By.XPATH, "//button[@type='submit' or contains(text(), 'Save') or contains(text(), 'Next') or contains(text(), 'Continue')]")

    def enter_address_line1(self, address):
        self.do_send_keys(self.ADDRESS_LINE_1, address)

    def enter_street_locality(self, street):
        self.do_send_keys(self.STREET_LOCALITY, street)

    def select_state(self, state):
        """Select state from Chosen.js dropdown."""
        self.select_chosen_option(self.STATE_CHOSEN, state)
        
    def select_district(self, district):
        """Select district from Chosen.js dropdown (must select state first)."""
        time.sleep(0.5)  # Quick wait for district dropdown to load after state selection
        self.select_chosen_option(self.DISTRICT_CHOSEN, district)

    def enter_pincode(self, pincode):
        self.do_send_keys(self.PINCODE_INPUT, pincode)
        
    def click_continue(self):
        self.do_click(self.CONTINUE_BTN)
