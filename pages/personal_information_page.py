from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class PersonalInformationPage(BasePage):
    # Locators
    # Using xpath contains to handle dynamic/unknown form prefixes
    CATEGORY_CHOSEN = (By.XPATH, "//div[contains(@id, 'social_category_chosen')]") 
    # Broader locator for Medium
    MEDIUM_CHOSEN = (By.XPATH, "//div[contains(@id, 'medium_of_study_chosen') or contains(@id, 'medium_chosen')]")
    
    # Generic submit button similar to Authentication Page
    CONTINUE_BTN = (By.XPATH, "//button[@type='submit' or contains(text(), 'Save') or contains(text(), 'Next') or contains(text(), 'Continue')]")

    def _element_exists(self, locator, timeout=3):
        """Check if an element exists on the page"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except:
            return False

    def _select_chosen_option(self, container_locator, option_text):
        # First check if the element exists
        if not self._element_exists(container_locator, timeout=5):
            self.logger.warning(f"Dropdown element {container_locator} not found on page, skipping selection. FORM SUBMISSION MAY FAIL.")
            return
            
        try:
            # Find the container element first to get its actual ID
            container_elem = self.driver.find_element(*container_locator)
            container_id = container_elem.get_attribute('id')
            
            # Scroll element into view to avoid footer blocking click
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", container_elem)
            time.sleep(0.5)  # Wait for scroll to complete
            
            if not container_id:
                self.logger.warning(f"Container has no ID, using direct element interaction")
                option_xpath = f".//ul[@class='chosen-results']/li[contains(text(), '{option_text}')]"
            else:
                option_xpath = f"//div[@id='{container_id}']//ul[@class='chosen-results']/li[contains(text(), '{option_text}')]"
        except Exception as e:
            self.logger.error(f"Could not find container element: {e}")
            return
        
        try:
            # Try 1: JS Click on container to open dropdown, then select option
            self.driver.execute_script("arguments[0].click();", container_elem)
            time.sleep(1)  # Wait for dropdown to fully open
            option_elem = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, option_xpath))
            )
            self.driver.execute_script("arguments[0].click();", option_elem)
            self.logger.info(f"Selected '{option_text}' from {container_id}")
            return
        except Exception as e:
            self.logger.warning(f"JS click strategy failed for {container_locator}: {e}. Trying ActionChains.")
        
        try:
            # Try 2: Use ActionChains for more reliable clicking
            from selenium.webdriver.common.action_chains import ActionChains
            actions = ActionChains(self.driver)
            actions.move_to_element(container_elem).click().perform()
            time.sleep(1)
            option_elem = self.driver.find_element(By.XPATH, option_xpath)
            actions.move_to_element(option_elem).click().perform()
            self.logger.info(f"Selected '{option_text}' from {container_id} using ActionChains")
            return
        except Exception as e:
            self.logger.error(f"All Chosen selection strategies failed for {container_locator}: {e}")
            pass

    def set_social_category(self, category):
        self._select_chosen_option(self.CATEGORY_CHOSEN, category)

    def set_medium_of_study(self, medium):
        self._select_chosen_option(self.MEDIUM_CHOSEN, medium)
        
    def click_continue(self):
        time.sleep(2)  # Wait for any page transitions
        try:
            self.do_click(self.CONTINUE_BTN)
        except:
             # Try JS Click if standard click fails
             btn = self.driver.find_element(*self.CONTINUE_BTN)
             self.driver.execute_script("arguments[0].click();", btn)
             self.logger.info("Clicked Continue using JS fallback")
