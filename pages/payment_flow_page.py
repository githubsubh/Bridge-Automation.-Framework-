from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import time

class PaymentFlowPage(BasePage):
    # Review Page Locators
    PAY_NOW_BTN = (By.XPATH, "//button[contains(text(), 'Pay Now')]")
    CONFIRM_CHECKBOX = (By.ID, "confirm_payment_review")
    
    # SabPaisa Payment Page Locators
    # These are illustrative based on typical gateway structures
    CARD_NUMBER_INPUT = (By.ID, "cardNumber") 
    CARD_HOLDER_INPUT = (By.ID, "cardHolderName")
    EXPIRY_INPUT = (By.ID, "cardExpiry")
    CVV_INPUT = (By.ID, "cardCvv")
    SUBMIT_PAYMENT_BTN = (By.ID, "submitPayment")
    
    def review_and_pay(self):
        # Review Page Actions
        try:
            self.do_click(self.CONFIRM_CHECKBOX)
        except:
            pass # Maybe already checked or not present
            
        self.logger.info("Clicking Pay Now on Review Page")
        self.do_click(self.PAY_NOW_BTN)
        
    def select_payment_mode(self, mode="Card"):
        # Select Card/Debit Card option on gateway
        # This is highly specific to the gateway UI
        xpath = f"//div[contains(text(), '{mode}')]"
        try:
            self.do_click((By.XPATH, xpath))
        except:
            self.logger.warning(f"Could not select payment mode {mode}")

    def enter_card_details(self, number, name, expiry, cvv):
        # Switch to iframe if needed (common in gateways)
        frames = self.driver.find_elements(By.TAG_NAME, "iframe")
        if frames:
            self.driver.switch_to.frame(frames[0])
            self.logger.info("Switched to payment iframe")
            
        self.do_send_keys(self.CARD_NUMBER_INPUT, number)
        self.do_send_keys(self.CARD_HOLDER_INPUT, name)
        self.do_send_keys(self.EXPIRY_INPUT, expiry)
        self.do_send_keys(self.CVV_INPUT, cvv)
        
        # Switch back if needed, but usually we click submit inside frame
        self.do_click(self.SUBMIT_PAYMENT_BTN)
        
        # Return to main content
        self.driver.switch_to.default_content()

