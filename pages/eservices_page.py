from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class EServicesPage(BasePage):
    # --- Locators: Apply Page ---
    container_services = (By.CSS_SELECTOR, ".c-table.d1 .container")
    list_service_items = (By.CSS_SELECTOR, "li.list-group-item")
    btn_apply_service = (By.CSS_SELECTOR, "a[title*='Apply for']")
    
    # --- Locators: My Requests Page ---
    table_requests = (By.CSS_SELECTOR, ".fee-details table.table-striped")
    rows_requests = (By.CSS_SELECTOR, ".fee-details table.table-striped tbody tr")
    header_my_requests = (By.XPATH, "//h1[contains(text(), 'Your E-Service Requests')]")
    
    def __init__(self, driver):
        super().__init__(driver)

    def get_service_count(self):
        """Returns number of available e-services to apply for."""
        items = self.driver.find_elements(*self.list_service_items)
        links = self.driver.find_elements(*self.btn_apply_service)
        self.logger.info(f"Available Services: {len(links)} found across {len(items)} items.")
        return len(links)

    def get_request_history(self):
        """Returns list of existing e-service requests."""
        self.logger.info("Scraping E-Service Request history...")
        rows = self.driver.find_elements(*self.rows_requests)
        requests = []
        
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 6:
                req_data = {
                    "request_id": cols[1].text.strip(),
                    "type": cols[2].text.strip(),
                    "status": cols[5].text.strip()
                }
                requests.append(req_data)
        
        return requests

    def verify_request_exists(self, request_type):
        """Checks if a request of a specific type exists in history."""
        reqs = self.get_request_history()
        for r in reqs:
            if request_type.lower() in r['type'].lower():
                self.logger.info(f"Confirmed request found: {r['type']} (Status: {r['status']})")
                return True
        return False
