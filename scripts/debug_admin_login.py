from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
try:
    driver.get("https://bridge-uat-admin.nios.ac.in")
    time.sleep(5)
    print("URL:", driver.current_url)
    print("Page Source Snippet:", driver.page_source[:2000])
    # Take a screenshot
    driver.save_screenshot("login_page_debug.png")
finally:
    driver.quit()
