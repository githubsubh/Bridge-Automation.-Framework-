from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class WaitUtils:
    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(self.driver, self.timeout)

    def visibility_wait(self, locator):
        """Wait for element to be visible."""
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not visible after {self.timeout}s")

    def clickable_wait(self, locator):
        """Wait for element to be clickable."""
        try:
            return self.wait.until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not clickable after {self.timeout}s")

    def presence_wait(self, locator):
        """Wait for element to be present in DOM."""
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not present after {self.timeout}s")

    def invisibility_wait(self, locator):
        """Wait for element to be invisible."""
        try:
            return self.wait.until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            raise TimeoutException(f"Element {locator} still visible after {self.timeout}s")

    def wait_for_url_contains(self, partial_url):
        """Wait for the URL to contain a specific string."""
        try:
            return self.wait.until(EC.url_contains(partial_url))
        except TimeoutException:
            raise TimeoutException(f"URL did not contain '{partial_url}' after {self.timeout}s. Current URL: {self.driver.current_url}")

    def wait_for_text_present(self, locator, text):
        """Wait for specific text to be present in an element."""
        try:
            return self.wait.until(EC.text_to_be_present_in_element(locator, text))
        except TimeoutException:
            raise TimeoutException(f"Text '{text}' not found in {locator} after {self.timeout}s")

    def wait_for_element_to_be_stale(self, element):
        """Wait for an element to go stale (e.g. after a page refresh)."""
        try:
            return self.wait.until(EC.staleness_of(element))
        except TimeoutException:
            raise TimeoutException(f"Element did not go stale after {self.timeout}s")
