from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class TransactionsPage(BasePage):
    # --- Locators ---
    table_transactions = (By.CSS_SELECTOR, "table.table-striped")
    columns_headers = (By.CSS_SELECTOR, "table.table-striped thead th")
    rows_data = (By.CSS_SELECTOR, "table.table-striped tbody tr")
    
    def __init__(self, driver):
        super().__init__(driver)

    def get_all_transactions(self):
        """Returns a list of dictionaries containing transaction details."""
        self.logger.info("Scraping Payment History table...")
        rows = self.driver.find_elements(*self.rows_data)
        transactions = []
        
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 8:
                tx_data = {
                    "module": cols[1].text.strip(),
                    "tx_id": cols[2].text.strip(),
                    "amount": cols[5].text.strip(),
                    "status": cols[6].text.strip(),
                    "date": cols[7].text.strip()
                }
                transactions.append(tx_data)
        
        return transactions

    def verify_all_paid(self):
        """Verifies that all transactions listed have a 'PAID' status."""
        txs = self.get_all_transactions()
        self.logger.info(f"Checking status for {len(txs)} transactions.")
        
        failures = []
        for tx in txs:
            if tx['status'] != "PAID":
                failures.append(f"TX {tx['tx_id']} is {tx['status']} (Expected PAID)")
        
        if not failures:
            self.logger.info("All transactions are verified as PAID.")
            return True
        else:
            for fail in failures:
                self.logger.error(fail)
            return False

    def download_first_receipt(self):
        """Clicks the download button for the first transaction and handles the new tab."""
        import time
        self.logger.info("Attempting to download the first receipt...")
        try:
            # Locate first download button
            btn_download = (By.XPATH, "//table[contains(@class,'table-striped')]//tbody/tr[1]//a[contains(text(),'Download')]")
            if self.is_visible(btn_download):
                self.do_click(btn_download)
                self.logger.info("Clicked 'Download'. Waiting for new tab...")
                time.sleep(3)
                
                # Switch to new tab and close it (to simulate verification)
                handles = self.driver.window_handles
                if len(handles) > 1:
                    self.logger.info("New tab detected. Switching to verify...")
                    self.driver.switch_to.window(handles[-1])
                    self.logger.info(f"Download Page URL: {self.driver.current_url}")
                    time.sleep(2)
                    self.driver.close()
                    self.driver.switch_to.window(handles[0])
                    self.logger.info("Closed download tab and returned to main window.")
                    return True
                else:
                    self.logger.warning("Download button clicked but no new tab opened.")
                    return False
            else:
                self.logger.error("Download button not found for first transaction.")
                return False
        except Exception as e:
            self.logger.error(f"Failed to download receipt: {e}")
            return False
