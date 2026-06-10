import os, sys, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DRIVER_PATH  = r"C:\Users\Insph\.wdm\drivers\chromedriver\win64\144.0.7559.133\chromedriver-win32\chromedriver.exe"
BASE_URL     = "https://bridge-uat.nios.ac.in/registration/basic-details"
SCREENSHOT   = os.path.join(os.path.dirname(__file__), "debug_screenshot.png")

options = Options()
options.add_argument("--start-maximized")

service = Service(executable_path=DRIVER_PATH)
driver  = webdriver.Chrome(service=service, options=options)

try:
    print(f"Navigating to: {BASE_URL}")
    driver.get(BASE_URL)
    time.sleep(3)

    # ── Try to dismiss modal ───────────────────────────────────────────────
    try:
        btn = WebDriverWait(driver, 4).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.swal2-confirm"))
        )
        modal_text = driver.find_element(By.CSS_SELECTOR, ".swal2-content, .swal2-html-container").text
        print(f"Modal visible. Text: {modal_text!r}")
        btn.click()
        print("Modal dismissed.")
        time.sleep(2)
    except Exception:
        print("No modal detected.")

    # ── Report state ───────────────────────────────────────────────────────
    print(f"\nCurrent URL  : {driver.current_url}")
    print(f"Page title   : {driver.title}")

    # Check if the name field exists in DOM
    elements = driver.find_elements(By.ID, "basicdetailform-name")
    print(f"Name field present in DOM: {len(elements) > 0}")
    if elements:
        print(f"  → Displayed : {elements[0].is_displayed()}")
        print(f"  → Enabled   : {elements[0].is_enabled()}")

    # Take screenshot
    driver.save_screenshot(SCREENSHOT)
    print(f"\nScreenshot saved → {SCREENSHOT}")

finally:
    input("\nPress ENTER to close browser...")
    driver.quit()
