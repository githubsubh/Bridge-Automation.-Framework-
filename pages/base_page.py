from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utilities.custom_logger import LogGen

class BasePage:
    logger = LogGen.loggen()

    def __init__(self, driver):
        self.driver = driver

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
