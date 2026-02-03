from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utilities.custom_logger import LogGen

class BasePage:
    logger = LogGen.loggen()

    def __init__(self, driver):
        self.driver = driver

    def select_chosen_option(self, container_locator, option_text):
        """Select an option from a Chosen.js dropdown."""
        from selenium.webdriver.common.by import By
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
            # Don't pass, let it bubble or handle if critical? 
            # If this fails, form submission will likely fail.
            pass

    def do_click(self, by_locator):
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator)).click()
            self.logger.info(f"Clicked on element with locator: {by_locator}")
        except Exception as e:
            self.logger.error(f"Exception occurred while clicking on element: {by_locator}. Exception: {e}")
            raise

    def do_send_keys(self, by_locator, text):
        try:
            # use clickable instead of just visible
            element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(by_locator))
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
            element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator))
            self.logger.info(f"Got text '{element.text}' from element with locator: {by_locator}")
            return element.text
        except Exception as e:
            self.logger.error(f"Exception occurred while getting text from element: {by_locator}. Exception: {e}")
            raise

    def is_visible(self, by_locator):
        try:
            element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator))
            return bool(element)
        except TimeoutException:
            return False
        except Exception as e:
            self.logger.error(f"Exception in is_visible for element: {by_locator}. Exception: {e}")
            return False

    def wait_for_invisibility(self, by_locator):
        try:
            WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located(by_locator))
            self.logger.info(f"Element with locator {by_locator} is now invisible")
        except Exception as e:
            self.logger.error(f"Exception while waiting for invisibility of {by_locator}: {e}")
