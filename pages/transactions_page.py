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
