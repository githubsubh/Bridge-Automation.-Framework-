from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class AddressDetailsPage(BasePage):
    # Locators
    # Updating to probable IDs based on pattern
    ADDRESS_LINE_1 = (By.ID, "addressdetailform-address_line1")
    STATE_CHOSEN = (By.ID, "addressdetailform-state_chosen")
    DISTRICT_CHOSEN = (By.ID, "addressdetailform-district_chosen")
    PINCODE_INPUT = (By.ID, "addressdetailform-pincode")
    
    CONTINUE_BTN = (By.XPATH, "//button[@type='submit' or contains(text(), 'Save') or contains(text(), 'Next') or contains(text(), 'Continue')]")

    def enter_address_line1(self, address):
        self.do_send_keys(self.ADDRESS_LINE_1, address)

    def select_state(self, state):
        self.select_chosen_option(self.STATE_CHOSEN, state)
        
    def select_district(self, district):
        # District usually depends on state, loading dynamically. 
        # chosen might refresh. sleep slightly or wait? BasePage click handles implicit wait.
        self.select_chosen_option(self.DISTRICT_CHOSEN, district)

    def enter_pincode(self, pincode):
        self.do_send_keys(self.PINCODE_INPUT, pincode)
        
    def click_continue(self):
        self.do_click(self.CONTINUE_BTN)
