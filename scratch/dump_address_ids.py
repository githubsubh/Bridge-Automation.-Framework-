import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def dump_address_ids():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # 1. Basic Details
        driver.get("https://bridge-uat.nios.ac.in/registration/basic-details")
        time.sleep(2)
        
        # Bypass modal
        try:
            driver.find_element(By.CSS_SELECTOR, "button.swal2-confirm").click()
        except: pass
        
        driver.find_element(By.ID, "basicdetailform-name").send_keys("DEBUG USER")
        driver.execute_script("document.getElementById('basicdetailform-date_of_birth').value = '15-08-1990'")
        
        # Gender (JS Click)
        gender_trigger = driver.find_element(By.ID, "basicdetailform_gender_chosen")
        driver.execute_script("arguments[0].click();", gender_trigger)
        time.sleep(0.5)
        male_option = driver.find_element(By.XPATH, "//li[contains(text(), 'Male')]")
        driver.execute_script("arguments[0].click();", male_option)
        
        driver.find_element(By.ID, "basicdetailform-udise_code").send_keys("09150101103")
        driver.execute_script("document.getElementById('verify-udise').click();")
        time.sleep(1)
        driver.execute_script("document.getElementById('submit-basic-details').click();")
        time.sleep(2)
        
        # 2. Authentication (Bypass OTP skip logic)
        WebDriverWait(driver, 20).until(EC.url_contains("authentication"))
        driver.find_element(By.ID, "authenticationform-email").send_keys("debug@test.com")
        driver.find_element(By.ID, "authenticationform-mobile_no").send_keys("9000000000")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(2)
        
        # 3. Personal Info
        WebDriverWait(driver, 20).until(EC.url_contains("personal"))
        # Select category
        driver.find_element(By.ID, "personalinformationform_social_category_chosen").click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, "//li[contains(text(), 'General')]").click()
        
        # Select medium
        driver.find_element(By.ID, "personalinformationform_study_medium_chosen").click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, "//li[contains(text(), 'English')]").click()
        
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(2)
        
        # 4. Address Details
        WebDriverWait(driver, 20).until(EC.url_contains("address"))
        print(f"Landed on URL: {driver.current_url}")
        
        print("\n--- DUMPING ALL INPUT IDs ON ADDRESS PAGE ---")
        inputs = driver.find_elements(By.TAG_NAME, "input")
        for inp in inputs:
            print(f"Input ID: {inp.get_attribute('id')} | Name: {inp.get_attribute('name')} | Type: {inp.get_attribute('type')}")
            
        print("\n--- DUMPING ALL SELECT IDs ON ADDRESS PAGE ---")
        selects = driver.find_elements(By.TAG_NAME, "select")
        for sel in selects:
            print(f"Select ID: {sel.get_attribute('id')} | Name: {sel.get_attribute('name')}")
            
        print("\n--- DUMPING ALL CHOSEN CONTAINER IDs ---")
        chosen = driver.find_elements(By.CSS_SELECTOR, "div[id$='_chosen']")
        for ch in chosen:
            print(f"Chosen ID: {ch.get_attribute('id')}")

    finally:
        driver.quit()

if __name__ == "__main__":
    dump_address_ids()
