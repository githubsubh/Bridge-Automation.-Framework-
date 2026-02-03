from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class PersonalInformationPage(BasePage):
    # Locators
    # Using xpath contains to handle dynamic/unknown form prefixes
    CATEGORY_CHOSEN = (By.XPATH, "//div[contains(@id, 'social_category_chosen')]") 
    MEDIUM_CHOSEN = (By.XPATH, "//div[contains(@id, 'medium_of_study_chosen')]")
    
    # Generic submit button similar to Authentication Page
    CONTINUE_BTN = (By.XPATH, "//button[@type='submit' or contains(text(), 'Save') or contains(text(), 'Next') or contains(text(), 'Continue')]")

    def _select_chosen_option(self, container_locator, option_text):
        container_id = container_locator[1]
        xpath = f"//div[@id='{container_id}']//ul[@class='chosen-results']/li[contains(text(), '{option_text}')]"
        
        try:
            # Try 1: Standard Interaction
            self.do_click(container_locator)
            self.do_click((By.XPATH, xpath))
            self.logger.info(f"Selected '{option_text}' from {container_id}")
            return
        except Exception as e:
            self.logger.warning(f"Standard Chosen click failed for {container_locator}: {e}. Trying JS fallback.")
        
        try:
            # Try 2: JS Click on Container + Standard Click on Option
            container_elem = self.driver.find_element(*container_locator)
            self.driver.execute_script("arguments[0].click();", container_elem)
            self.do_click((By.XPATH, xpath))
            self.logger.info(f"Selected '{option_text}' from {container_id} using JS Container Click")
            return
        except Exception as e:
             self.logger.warning(f"JS Container click failed: {e}. Trying JS Click on Option directly.")

        try:
            # Try 3: JS Click on Option Directly (if pre-loaded/hidden)
            option_elem = self.driver.find_element(By.XPATH, xpath)
            self.driver.execute_script("arguments[0].click();", option_elem)
            self.logger.info(f"Selected '{option_text}' from {container_id} using fully JS Click")
        except Exception as e:
            self.logger.error(f"All Chosen selection strategies failed for {container_locator}: {e}")
            pass

    def set_social_category(self, category):
        self._select_chosen_option(self.CATEGORY_CHOSEN, category)

    def set_medium_of_study(self, medium):
        self._select_chosen_option(self.MEDIUM_CHOSEN, medium)
        
    def click_continue(self):
        self.do_click(self.CONTINUE_BTN)
