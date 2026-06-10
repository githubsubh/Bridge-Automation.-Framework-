import sys
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument('--headless=new')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

try:
    print("Launching Chromium...")
    driver = webdriver.Chrome(options=options)
    url = "https://digieval-uat.nios.ac.in/registration/basic-details"
    print(f"Connecting to {url} ...")
    driver.get(url)
    driver.implicitly_wait(10)
    time.sleep(2)
    
    # Handle the Restricted Access modal
    print("Checking for restricted access modal...")
    try:
        password_xpath = "//input[@type='password' or @placeholder='Enter Access Password']"
        elements = driver.find_elements(By.XPATH, password_xpath)
        if elements and elements[0].is_displayed():
            print("Restricted Access prompt detected. Entering password...")
            elements[0].send_keys("LetMeIn2026")
            time.sleep(0.5)
            submit_xpath = "//button[contains(text(), 'Submit')]"
            driver.find_element(By.XPATH, submit_xpath).click()
            time.sleep(2)
            print("Restricted Access prompt cleared.")
    except Exception as e:
        print("No restricted access modal or failed:", e)

    # Scrape limits
    print("Scraping Basic Details DOM...")
    
    # Wait for the main form to be visible (name input from POM is basicdetailform-name)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "basicdetailform-name")))
    except:
        print("Wait for form failed, but continuing scrape...")
        
    inputs = driver.find_elements(By.TAG_NAME, 'input')
    selects = driver.find_elements(By.TAG_NAME, 'select')
    
    results = []
    print(f"Found {len(inputs)} inputs and {len(selects)} selects on the page.")
    
    for el in inputs + selects:
        try:
            element_id = el.get_attribute('id') or ''
            name = el.get_attribute('name') or ''
            type_attr = el.get_attribute('type') or ''
            maxlength = el.get_attribute('maxlength') or ''
            minlength = el.get_attribute('minlength') or ''
            pattern = el.get_attribute('pattern') or ''
            required = el.get_attribute('required') or ''
            
            # Only care about elements with IDs or notable names
            if element_id or name:
                results.append(f"ID: {element_id} | Name: {name} | Type: {type_attr} | MaxLen: {maxlength} | MinLen: {minlength} | Req: {required}")
        except Exception:
            pass
            
    for r in results:
        print(r)
        
    driver.quit()
    print("Execution complete.")
except Exception as e:
    print('Critical Error:', str(e))
