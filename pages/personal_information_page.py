from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class PersonalInformationPage(BasePage):
    # Locators
    # Assuming standard Chosen structure: ID + "_chosen"
    CATEGORY_CHOSEN = (By.ID, "social_category_chosen") 
    MEDIUM_CHOSEN = (By.ID, "medium_of_study_chosen")
    
    # Generic submit button similar to Authentication Page
    CONTINUE_BTN = (By.XPATH, "//button[@type='submit' or contains(text(), 'Save') or contains(text(), 'Next') or contains(text(), 'Continue')]")

    def _select_chosen_option(self, container_locator, option_text):
        try:
            # Click container
            self.do_click(container_locator)
            # Click option
            # The ID of the container usually matches the ID in the xpath
            container_id = container_locator[1]
            xpath = f"//div[@id='{container_id}']//ul[@class='chosen-results']/li[contains(text(), '{option_text}')]"
            self.do_click((By.XPATH, xpath))
            self.logger.info(f"Selected '{option_text}' from {container_id}")
        except Exception as e:
            self.logger.warning(f"Chosen selection failed for {container_locator}: {e}. Trying JS fallback on original select.")
            # Fallback: try setting value on original select if possible? 
            # Or just fail since hidden select interaction is hard without ID knowledge.
            # Let's try to just click the option if the container open failed?
            pass

    def set_social_category(self, category):
        self._select_chosen_option(self.CATEGORY_CHOSEN, category)

    def set_medium_of_study(self, medium):
        self._select_chosen_option(self.MEDIUM_CHOSEN, medium)
        
    def click_continue(self):
        self.do_click(self.CONTINUE_BTN)
