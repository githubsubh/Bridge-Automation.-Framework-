from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    
    def check_all_confirmation_boxes(self):
        """Toggle all checkboxes on the review page using robust JS clicks."""
        try:
            # Wait for checkboxes to be present
            WebDriverWait(self.driver, self.TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='checkbox']")))
            # Find all checkboxes
            checkboxes = self.driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
            self.logger.info(f"Found {len(checkboxes)} checkboxes on Review page.")
            
            for cb in checkboxes:
                try:
                    # Scroll to and click using JS to handle potential overlaps/unclickable states
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", cb)
                    if not cb.is_selected():
                        self.driver.execute_script("arguments[0].click();", cb)
                        self.logger.info("Clicked checkbox via JS")
                    else:
                        self.logger.info("Checkbox already selected")
                except Exception as e:
                    self.logger.warning(f"Failed to click checkbox: {e}")
        except Exception as e:
            self.logger.warning(f"Error handling checkboxes: {e}")

    def select_sabpaisa_gateway(self):
        """Select SabPaisa gateway by finding its text label."""
        try:
            self.logger.info("Searching for SabPaisa gateway...")
            # time.sleep(2) # Removed redundant wait
            
            # Specific Locator as per User Request:
            # <input type="radio" id="gateway_sab-paisa" ...>
            
            try:
                # Direct locator for the exact radio button
                sab_paisa_radio = self.driver.find_element(By.ID, "gateway_sab-paisa")
                
                # Check if we need to click the sibling label or parent if the radio is hidden
                if not sab_paisa_radio.is_displayed():
                     # Attempt to click parent label usually wrapping it, or use JS
                     self.driver.execute_script("arguments[0].click();", sab_paisa_radio)
                     self.logger.info("Clicked SabPaisa radio via JS (ID: gateway_sab-paisa)")
                else:
                    sab_paisa_radio.click()
                    self.logger.info("Clicked SabPaisa radio directly (ID: gateway_sab-paisa)")
                return True
            except Exception as e:
                self.logger.warning(f"Direct ID 'gateway_sab-paisa' failed: {e}. Falling back...")

            # Fallback 1: CSS Attribute Selector for value='sab-paisa'
            try:
                el = self.driver.find_element(By.CSS_SELECTOR, "input[value='sab-paisa']")
                self.driver.execute_script("arguments[0].click();", el)
                self.logger.info("Clicked SabPaisa via value='sab-paisa'")
                return True
            except:
                pass
                
            # Fallback 2: Previous Text-based Logic
            xpath = "//*[contains(text(), 'SabPaisa') or contains(text(), 'Sab Paisa')]"
            elements = self.driver.find_elements(By.XPATH, xpath)
            
            for el in elements:
                try:
                    if el.is_displayed():
                        el.click()
                        self.logger.info("Clicked SabPaisa text element")
                        return True
                except:
                    pass
                
                # Try clicking the parent (often the label or row)
                try:
                    parent = el.find_element(By.XPATH, "./..")
                    self.driver.execute_script("arguments[0].click();", parent)
                    self.logger.info("Clicked SabPaisa parent element")
                    return True
                except:
                    pass

            # Fallback: Try ID if text fails (rare case)
            try:
                el = self.driver.find_element(By.ID, "gateway_1")
                self.driver.execute_script("arguments[0].click();", el)
                self.logger.info("Clicked gateway_1 ID")
                return True
            except:
                pass
                
            self.logger.error("Could not find SabPaisa gateway!")
            return False
        except Exception as e:
            self.logger.error(f"Error selecting SabPaisa: {e}")
            return False

    def click_pay_now(self):
        """Final click to proceed to payment gateway."""
        try:
            btn = self.driver.find_element(*self.PAY_NOW_BTN)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
            self.driver.execute_script("arguments[0].click();", btn)
            self.logger.info("Clicked Pay Now button")
        except:
             # Try generic submit
             self.do_click((By.XPATH, "//button[@type='submit' or contains(text(), 'Pay')]"))
        
    def select_payment_mode(self, mode="Credit Card"):
        """Select payment mode on SabPaisa gateway."""
        try:
            # Common patterns for gateway mode buttons
            self.logger.info(f"Attempting to select payment mode: {mode}")
            # time.sleep(2)  # Removed redundant wait
            
            # Try finding by text or specific common classes
            locators = [
                (By.XPATH, f"//*[contains(text(), '{mode}')]"),
                (By.XPATH, "//li[contains(@class, 'payment-mode')]"),
                (By.XPATH, "//button[contains(@class, 'card')]"),
                (By.CSS_SELECTOR, ".card-payment-option")
            ]
            
            for by, val in locators:
                try:
                    el = self.driver.find_element(by, val)
                    self.driver.execute_script("arguments[0].click();", el)
                    self.logger.info(f"Selected mode via {val}")
                    return True
                except:
                    continue
            return False
        except Exception as e:
            self.logger.warning(f"Could not select payment mode {mode}: {e}")
            return False

    def enter_card_details(self, number, name, expiry, cvv):
        """Enter dummy card details on SabPaisa gateway with robust detection."""
        try:
            self.logger.info(f"Entering card details for: {name}")
            # time.sleep(2) # Wait for form transition - replaced with explicit wait below

            # Retry loop to find fields (handling potential loading delays)
            found_fields = False
            for attempt in range(5):
                # 1. Search for potential iframes
                iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
                self.logger.info(f"Attempt {attempt+1}: Found {len(iframes)} iframes.")
                
                card_field_selectors = [
                     (By.ID, "cardNumber"), (By.NAME, "cardNumber"), (By.CSS_SELECTOR, "input[name*='card'][name*='number']"),
                     (By.ID, "cardNum"), (By.CSS_SELECTOR, "input[placeholder*='Number']")
                ]

                def find_fields():
                    for by, sel in card_field_selectors:
                        if self.driver.find_elements(by, sel):
                            return True
                    return False

                # Check main frame first
                if find_fields():
                    found_fields = True
                    break
                
                # Check iframes
                iframe_found = False
                for i, frame in enumerate(iframes):
                    try:
                        self.driver.switch_to.frame(frame)
                        if find_fields():
                            self.logger.info(f"Found card fields in iframe {i}")
                            iframe_found = True
                            found_fields = True
                            break
                        self.driver.switch_to.default_content()
                    except:
                        self.driver.switch_to.default_content()
                
                if iframe_found:
                    break
                
                if not found_fields:
                    self.logger.info("Card fields not found yet, waiting...")
                    time.sleep(2)
            
            if not found_fields:
                self.logger.error("Failed to find card details fields after retries.")


            # 2. Enter details using prioritized locators
            field_maps = [
                {"sel": ["#cardNumber", "[name='cardNumber']", "input[name*='number']"], "val": number},
                {"sel": ["#cardHolderName", "[name='cardHolderName']", "input[name*='name']"], "val": name},
                {"sel": ["#cardExpiry", "[name='cardExpiry']", "input[name*='expiry']", "input[placeholder*='MM/YY']"], "val": expiry},
                {"sel": ["#cardCvv", "[name='cardCvv']", "input[name*='cvv']", "input[placeholder*='CVV']"], "val": cvv}
            ]

            for field in field_maps:
                for selector in field["sel"]:
                    try:
                        el = self.driver.find_element(By.CSS_SELECTOR, selector)
                        el.clear()
                        el.send_keys(field["val"])
                        self.logger.info(f"Set field via {selector}")
                        break # Found it, move to next field
                    except:
                        continue

            # 3. Click Pay/Submit
            try:
                pay_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Pay') or contains(text(), 'Submit') or @id='payBtn' or @id='submitPayment']")
                self.driver.execute_script("arguments[0].click();", pay_btn)
                self.logger.info("Clicked Pay on gateway")
            except:
                # Last resort: try any primary button
                self.driver.execute_script("document.querySelector('button.btn-primary, button[type=submit]').click();")

            self.driver.switch_to.default_content()
        except Exception as e:
            self.logger.error(f"Error in enter_card_details: {e}")

    def simulate_success(self):
        """Handle the success/fail simulation page."""
        try:
            self.logger.info("Waiting for Success/Fail simulation page...")
            WebDriverWait(self.driver, self.TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Success') or contains(@id, 'success')]")))
            success_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Success') or contains(@id, 'success')]")
            self.driver.execute_script("arguments[0].click();", success_btn)
            self.logger.info("Clicked Success on simulation page")
        except Exception as e:
            self.logger.warning(f"Could not find Success button: {e}")

