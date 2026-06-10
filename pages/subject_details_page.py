from pages.base_page import BasePage
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SubjectDetailsPage(BasePage):
    # Locators for 7 subjects - assuming they are dropdowns or checkboxes
    # Restoring as generic method to select medium for all
    
    # Updated based on debug logs
    CONTINUE_BTN = (By.ID, "submitbtnv")

    def select_medium_for_subject(self, subject_index, medium):
        # IDs use words: one, two, three...
        words = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven"}
        word = words.get(subject_index, str(subject_index))
        # Target the SELECT element directly (BasePage will handle unhiding if needed)
        locator = (By.ID, f"subjectdetailsform-subject_{word}_medium")
        self.select_chosen_option(locator, medium)
        
    def select_any_medium_for_enabled_subjects(self):
        words = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven"}
        
        self.logger.info("Auto-detecting enabled subject medium dropdowns...")
        for i in range(1, 8):
            word = words.get(i, str(i))
            # Try both word-based and number-based IDs
            locators = [
                (By.ID, f"subjectdetailsform-subject_{word}_medium"),
                (By.ID, f"subjectdetailsform-subject_{i}_medium"),
                (By.ID, f"subjectdetailsform-subject_{word}_medium_id"),
                (By.ID, f"subjectdetailsform-subject_{i}_medium_id")
            ]
            
            for locator in locators:
                try:
                    # Check if element exists in DOM
                    elements = self.driver.find_elements(*locator)
                    if not elements:
                         continue
                         
                    elem = elements[0]
                    self.logger.info(f"Found element for Subject {i} using {locator[1]}. Displayed: {elem.is_displayed()}, Enabled: {elem.is_enabled()}")
                    
                    if not elem.is_enabled():
                        self.logger.info(f"Subject {i} ({word}) medium is disabled.")
                        continue

                    self.logger.info(f"Attempting to select 'Any' for Subject {i}...")
                    result = self.select_chosen_option(locator, "Any")
                    if result:
                        self.logger.info(f"Successfully selected 'Any' for Subject {i}")
                        break # Move to next subject
                except Exception as e:
                    self.logger.debug(f"Locator {locator} failed for subject {i}: {e}")
                    continue
            else:
                self.logger.warning(f"Could not find any valid dropdown locator for Subject {i}")

    def debug_print_ids(self):
        import time
        self.logger.info("--- DEBUGGING LOCATORS ---")
        time.sleep(2) # Wait for load
        # Find all buttons and inputs
        elements = self.driver.find_elements(By.XPATH, "//*[self::button or self::input]")
        for elem in elements:
            try:
                eid = elem.get_attribute("id")
                tag = elem.tag_name
                etype = elem.get_attribute("type")
                text = elem.text
                if not text and tag == "input":
                    text = elem.get_attribute("value")
                
                self.logger.info(f"Element: Tag='{tag}', ID='{eid}', Type='{etype}', Text='{text}'")
            except:
                pass
        self.logger.info("--- END DEBUGGING ---")

    def click_continue(self):
        import time
        from selenium.webdriver.common.action_chains import ActionChains

        # Check if already navigated
        if "document" in self.driver.current_url.lower():
            self.logger.info("Already on Documents page.")
            return

        # Strategy 1: JS Click (Force)
        try:
             btn = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.CONTINUE_BTN))
             self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
             self.driver.execute_script("arguments[0].click();", btn)
             self.logger.info("Clicked Continue using JS (Force)")
        except Exception as e:
             self.logger.error(f"JS Click failed: {e}")

        # Targeted wait for navigation instead of fixed sleep
        try:
             WebDriverWait(self.driver, 5).until(EC.url_contains("document"))
             return
        except:
             pass

        # Strategy 2: ActionChains
        try:
             self.logger.warning("Page didn't navigate. Trying ActionChains...")
             btn = self.driver.find_element(*self.CONTINUE_BTN)
             ActionChains(self.driver).move_to_element(btn).click().perform()
             self.logger.info("Clicked Continue using ActionChains")
        except Exception as e:
             self.logger.error(f"ActionChains failed: {e}")

        try:
             WebDriverWait(self.driver, 5).until(EC.url_contains("document"))
             return
        except:
             pass

        # Strategy 3: Standard Click
        try:
             self.logger.warning("Still on page. Trying Standard Click...")
             self.do_click(self.CONTINUE_BTN)
        except Exception as e:
             self.logger.error(f"Standard Click failed: {e}")

        time.sleep(3)
        if "document" in self.driver.current_url.lower(): return

        # If we are here, we are stuck. Print page text to find errors.
        self.logger.error("FAILED TO NAVIGATE from Subject Details. DUMPING PAGE STATE:")
        
        # Check for error messages
        errors = self.driver.find_elements(By.CSS_SELECTOR, ".error, .alert, .text-danger, .help-block")
        for err in errors:
            if err.is_displayed() and err.text.strip():
                self.logger.error(f"Found Page Error: {err.text}")

        try:
             self.logger.info("Nuclear Option: Forcing form submission via JS...")
             self.driver.execute_script("document.getElementById('subject-details-form').submit();")
             time.sleep(5)
             if "document" in self.driver.current_url.lower(): 
                 self.logger.info("Nuclear submission successful!")
                 return
        except:
             pass
            
        raise Exception("Failed to navigate from Subject Details page")
