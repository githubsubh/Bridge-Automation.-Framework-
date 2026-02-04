from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utilities.custom_logger import LogGen
from utilities.read_properties import ReadConfig

class BasePage:
    logger = LogGen.loggen()
    TIMEOUT = ReadConfig.getExplicitWait()
    POLL_FREQUENCY = 0.5

    def __init__(self, driver):
        self.driver = driver

    def select_chosen_option(self, container_locator, option_text):
        """Robust Chosen.js dropdown selection with multiple strategies."""
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import Select
        import time
        
        # Check if it's a regular select element first (works for hidden selects if we unhide)
        try:
            element = self.driver.find_element(*container_locator)
            if element.tag_name == 'select':
                self.logger.info(f"Found regular select element, using Select class")
                
                # Unhide if hidden (e.g. if covered by Chosen)
                if not element.is_displayed():
                    self.logger.info("Select element is hidden, unhiding it...")
                    self.driver.execute_script("arguments[0].style.display = 'block';", element)
                    self.driver.execute_script("arguments[0].style.opacity = '1';", element)
                    self.driver.execute_script("arguments[0].style.visibility = 'visible';", element)
                    time.sleep(0.5)

                select = Select(element)
                
                # Check options
                try:
                    if len(select.options) <= 1:
                        # Wait for options if empty
                         time.sleep(2)
                         select = Select(self.driver.find_element(*container_locator))
                except:
                     pass
                     
                # Select by text
                try:
                    if option_text == "Any":
                        if len(select.options) > 1:
                            select.select_by_index(1)
                            self.logger.info(f"Selected index 1 (Any) from select dropdown")
                            self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", element)
                            return True
                    
                    select.select_by_visible_text(option_text)
                    self.logger.info(f"Selected '{option_text}' from select dropdown")
                    # Trigger change event
                    self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", element)
                    return True
                except:
                     # Try case insensitive
                     for opt in select.options:
                         if option_text.lower() in opt.text.lower():
                             select.select_by_visible_text(opt.text)
                             self.logger.info(f"Selected '{opt.text}' (partial match)")
                             self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", element)
                             return True
                     raise Exception(f"Option '{option_text}' not found in select")
        except Exception as e:
            if "not found" in str(e):
                 self.logger.warning(f"Select logic failed: {e}")
            pass

        # Extract ID if locator is ID based (common for Chosen)
        dropdown_id = None
        if container_locator[0] == By.ID:
            dropdown_id = container_locator[1]
        elif container_locator[0] == By.XPATH and "id(" in container_locator[1]:
             # strict extraction if needed, but ID locator is best
             pass
             
        if not dropdown_id:
             self.logger.warning(f"select_chosen_option: Could not extract ID from {container_locator}. Falling back to basic click.")
             # Fallback to simple click if not an ID we can parse easily for the robust method
             try:
                 element = self.driver.find_element(*container_locator)
                 element.click()
                 xpath = f"//li[contains(text(), '{option_text}')]"
                 WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, xpath))).click()
                 return
             except Exception as e:
                 self.logger.error(f"Basic fallback failed: {e}")
                 return

        try:
            # Strategies for UI Interaction
            # Strategy 1: Targeted Click on the trigger element
            try:
                # The ID passed is usually the container ID (e.g., state_dropdown_2_chosen)
                # The trigger is usually an 'a' tag with class 'chosen-single' inside it
                trigger_xpath = f"//div[@id='{dropdown_id}']/a[contains(@class, 'chosen-single')]"
                try:
                    trigger = WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.XPATH, trigger_xpath)))
                except:
                    # Maybe it's a multi-select?
                    trigger_xpath = f"//div[@id='{dropdown_id}']/ul[contains(@class, 'chosen-choices')]"
                    trigger = WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.XPATH, trigger_xpath)))

                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", trigger)
                time.sleep(1)
                
                # Click to open
                self.logger.info(f"Clicking trigger for {dropdown_id}")
                trigger.click()
                time.sleep(1)
                
                # Check for results
                results_xpath = f"//div[@id='{dropdown_id}']//ul[@class='chosen-results']"
                if self.is_visible((By.XPATH, results_xpath)):
                     # Get all list items
                    items_xpath = f"//div[@id='{dropdown_id}']//ul[@class='chosen-results']/li"
                    items = self.driver.find_elements(By.XPATH, items_xpath)
                    
                    self.logger.info(f"Found {len(items)} items in dropdown {dropdown_id}")
                    
                    # Find and click the matching option
                    for item in items:
                        item_text = item.text.strip()
                        if option_text.lower() in item_text.lower(): # Case insensitive check
                            self.logger.info(f"Clicking on option: '{item_text}'")
                            item.click()
                            time.sleep(1)
                            self.logger.info(f"Selected '{item_text}' from {dropdown_id}")
                            return True
            except Exception as e:
                self.logger.warning(f"UI Selection Strategy failed for {dropdown_id}: {e}")

            # Strategy 2: Fallback - Manipulate the underlying SELECT element
            self.logger.info(f"Attempting Fallback Strategy for {dropdown_id}")
            
            # Infer the original select ID
            # Usually Chosen ID is {original_id}_chosen
            original_select_id = dropdown_id.replace("_chosen", "")
            
            select_elem = self.driver.find_element(By.ID, original_select_id)
            
            # Make it visible just in case selenium refuses to interact
            self.driver.execute_script("arguments[0].style.display = 'block';", select_elem)
            time.sleep(0.5)
            
            select = Select(select_elem)
            
            # Select by text
            try:
                select.select_by_visible_text(option_text)
                self.logger.info(f"Fallback: Selected '{option_text}' using Select class")
            except:
                 # Try case insensitive
                 found = False
                 for opt in select.options:
                     if option_text.lower() in opt.text.lower():
                         select.select_by_visible_text(opt.text)
                         self.logger.info(f"Fallback: Selected '{opt.text}' (partial match) using Select class")
                         found = True
                         break
                 if not found:
                     raise Exception(f"Option '{option_text}' not found in underlying select")

            # Trigger events to ensure listeners (like dependent dropdowns) fire
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", select_elem)
            try:
                self.driver.execute_script(f"$('#{original_select_id}').trigger('chosen:updated');") # If jQuery is present
            except:
                pass
            time.sleep(1)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error selecting from {dropdown_id}: {e}")
            return False

    def do_click(self, by_locator):
        try:
            WebDriverWait(self.driver, self.TIMEOUT).until(EC.visibility_of_element_located(by_locator)).click()
            self.logger.info(f"Clicked on element with locator: {by_locator}")
        except Exception as e:
            self.logger.error(f"Exception occurred while clicking on element: {by_locator}. Exception: {e}")
            raise

    def do_send_keys(self, by_locator, text):
        try:
            # use clickable instead of just visible
            element = WebDriverWait(self.driver, self.TIMEOUT).until(EC.element_to_be_clickable(by_locator))
            # clear field first
            try:
                element.clear()
                element.send_keys(text)
            except Exception as e:
                self.logger.warning(f"Standard send_keys failed ({type(e).__name__}), trying JS: {e}")
                self.driver.execute_script("arguments[0].value = arguments[1];", element, text)
                self.driver.execute_script("arguments[0].dispatchEvent(new Event('input'));", element)
                self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", element)
                self.driver.execute_script("arguments[0].dispatchEvent(new Event('blur'));", element)
                
            self.logger.info(f"Sent keys '{text}' to element with locator: {by_locator}")
        except Exception as e:
            self.logger.error(f"Exception occurred while sending keys to element: {by_locator}. Type: {type(e).__name__}. Exception: {e}")
            raise

    def get_element_text(self, by_locator):
        try:
            element = WebDriverWait(self.driver, self.TIMEOUT).until(EC.visibility_of_element_located(by_locator))
            self.logger.info(f"Got text '{element.text}' from element with locator: {by_locator}")
            return element.text
        except Exception as e:
            self.logger.error(f"Exception occurred while getting text from element: {by_locator}. Exception: {e}")
            raise

    def is_visible(self, by_locator):
        try:
            element = WebDriverWait(self.driver, self.TIMEOUT).until(EC.visibility_of_element_located(by_locator))
            return bool(element)
        except TimeoutException:
            return False
        except Exception as e:
            self.logger.error(f"Exception in is_visible for element: {by_locator}. Exception: {e}")
            return False

    def wait_for_invisibility(self, by_locator):
        try:
            WebDriverWait(self.driver, self.TIMEOUT).until(EC.invisibility_of_element_located(by_locator))
            self.logger.info(f"Element with locator {by_locator} is now invisible")
        except Exception as e:
            self.logger.error(f"Exception while waiting for invisibility of {by_locator}: {e}")
