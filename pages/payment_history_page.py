from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time

class PaymentHistoryPage(BasePage):
    # Locators
    # We assume standard table structure or list of cards based on typical bootstrap themes
    # Looking for generically "Download" buttons or Receipt icons
    
    # This xpath looks for any anchor tag that contains 'Download' text or has a download icon class
    # Adjusting to be broad to catch multiple potential implementations
    link_download_receipt_xpath = (By.XPATH, "//a[contains(text(), 'Download') or contains(@class, 'fa-download')]")
    
    table_rows_xpath = (By.XPATH, "//table/tbody/tr")
    
    def __init__(self, driver):
        super().__init__(driver)

    def download_all_receipts(self):
        """Finds and clicks all receipt download links on the page."""
        self.logger.info("Scanning for Payment Receipts to download...")
        
        # Give a moment for table to load
        time.sleep(2)
        
        downloads = self.driver.find_elements(*self.link_download_receipt_xpath)
        count = len(downloads)
        
        self.logger.info(f"Found {count} download link(s).")
        
        if count == 0:
            self.logger.warning("No receipt download links found. If this is unexpected, check locators.")
            return 0

        success_count = 0
        for index in range(count):
            # Re-find elements to avoid StaleElementReferenceException if page refreshes or DOM changes
            downloads = self.driver.find_elements(*self.link_download_receipt_xpath)
            if index < len(downloads):
                link = downloads[index]
                try:
                    href = link.get_attribute("href")
                    self.logger.info(f"Downloading Receipt {index+1}: {href}")
                    link.click()
                    success_count += 1
                    time.sleep(2) # Wait for download to start/complete before next
                except Exception as e:
                    self.logger.error(f"Failed to click download link {index+1}: {e}")
            else:
                self.logger.warning(f"Download link {index+1} no longer found.")

        self.logger.info(f"Successfully initiated {success_count} downloads.")
        return success_count
