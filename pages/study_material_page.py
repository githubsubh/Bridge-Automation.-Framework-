from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time

class StudyMaterialPage(BasePage):
    # Locators
    # Assuming similar structure: a table or list with download links
    # We'll look for generic download buttons/icons or links ending in .pdf
    
    # Generic locator for download links in a table/list context
    link_download_material_xpath = (By.XPATH, "//a[contains(text(), 'Download') or contains(@class, 'fa-download') or contains(@href, '.pdf')]")
    
    def __init__(self, driver):
        super().__init__(driver)

    def download_all_materials(self):
        """Finds and clicks all study material download links."""
        self.logger.info("Scanning for Study Materials to download...")
        
        time.sleep(2) # Wait for page load
        
        downloads = self.driver.find_elements(*self.link_download_material_xpath)
        count = len(downloads)
        
        self.logger.info(f"Found {count} study material download link(s).")
        
        if count == 0:
            self.logger.warning("No study material download links found. This is expected if content is not yet uploaded.")
            self.logger.info("Automation Logic: Scanned page for links matching 'Download' or '.pdf'. None found.")
            return 0

        success_count = 0
        for index in range(count):
            try:
                # Re-find to avoid stale elements
                downloads = self.driver.find_elements(*self.link_download_material_xpath)
                if index < len(downloads):
                    link = downloads[index]
                    href = link.get_attribute("href")
                    
                    self.logger.info(f"Targeting Material {index+1}: {href}")
                    self.logger.info("Waiting 5 seconds for user to observe action...")
                    time.sleep(5) # User requested wait for visibility
                    
                    link.click()
                    self.logger.info(f"Clicked download link for {href}")
                    
                    success_count += 1
                    time.sleep(2) # Buffer for download start
            except Exception as e:
                self.logger.error(f"Failed to download material {index+1}: {e}")

        self.logger.info(f"Successfully initiated {success_count} downloads.")
        return success_count
