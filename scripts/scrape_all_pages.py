import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def js_click(dr, element):
    dr.execute_script("arguments[0].click();", element)

def js_type(dr, element, text):
    dr.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', {bubbles:true})); arguments[0].dispatchEvent(new Event('change', {bubbles:true}));", element, text)

def scrape_current_page(driver, page_name):
    print(f"--- Scraping Constraints for {page_name} ---")
    inputs = driver.find_elements(By.TAG_NAME, 'input')
    selects = driver.find_elements(By.TAG_NAME, 'select')
    
    for el in inputs + selects:
        try:
            val_id = el.get_attribute('id') or ''
            val_name = el.get_attribute('name') or ''
            type_attr = el.get_attribute('type') or ''
            maxl = el.get_attribute('maxlength') or ''
            minl = el.get_attribute('minlength') or ''
            pat = el.get_attribute('pattern') or ''
            clz = el.get_attribute('class') or ''
            if val_id or val_name:
                print(f"[{page_name}] ID: {val_id} | Name: {val_name} | Type: {type_attr} | MaxLen: {maxl} | MinLen: {minl} | Class: {clz}")
        except Exception: pass
    print("-" * 50)

options = Options()
profile_path = os.path.join(os.getcwd(), "automation_profiles", f"profile_live_scrape")
os.makedirs(profile_path, exist_ok=True)
options.add_argument(f"--user-data-dir={profile_path}")
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

try:
    print("Launching Chromium...")
    old_path = os.environ.get("PATH", "")
    clean_paths = [p for p in old_path.split(";") if "Python313\\Scripts" not in p]
    os.environ["PATH"] = ";".join(clean_paths)
    
    driver = webdriver.Chrome(options=options)
    os.environ["PATH"] = old_path
    driver.maximize_window()
    
    # 1. Basic Details
    driver.get("https://digieval-uat.nios.ac.in/registration/basic-details")
    driver.implicitly_wait(5)
    
    # Handle access modal
    try:
        pas = driver.find_elements(By.XPATH, "//input[@type='password' or @placeholder='Enter Access Password']")
        if pas and pas[0].is_displayed():
            js_type(driver, pas[0], "LetMeIn2026")
            js_click(driver, driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]"))
            time.sleep(2)
    except: pass

    # Scrape BD again just in case, but we mainly want to proceed
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "basicdetailform-name")))
    
    print("Filling Basic Details to proceed...")
    js_type(driver, driver.find_element(By.ID, "basicdetailform-name"), "TEST USER")
    js_type(driver, driver.find_element(By.ID, "basicdetailform-date_of_birth"), "10-10-1990")
    
    # Select Gender safely bypassing modals
    js_click(driver, driver.find_element(By.ID, "basicdetailform_gender_chosen"))
    time.sleep(0.5)
    js_click(driver, driver.find_element(By.XPATH, "//div[@id='basicdetailform_gender_chosen']//li[contains(text(), 'Male')]"))
    
    js_type(driver, driver.find_element(By.ID, "basicdetailform-aadhaar_no"), "987654321012")
    js_type(driver, driver.find_element(By.ID, "basicdetailform-pan"), "ABCDE1234F")
    
    # Submit safely via JS
    js_click(driver, driver.find_element(By.XPATH, "//button[contains(text(), 'Continue') or contains(text(), 'Save')]"))
    time.sleep(1)
    
    # Overcome 'Are you sure' swal modal
    try:
        swal_ok = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.swal2-confirm")))
        js_click(driver, swal_ok)
    except: pass

    # 2. Authentication
    WebDriverWait(driver, 15).until(lambda d: "authentication" in d.current_url.lower())
    print("Basic Details completed. Now at Auth.")
    
    js_type(driver, driver.find_element(By.ID, "authenticationform-email"), "subh7409+740@gmail.com")
    js_type(driver, driver.find_element(By.ID, "authenticationform-mobile_no"), "8287461243")
    js_click(driver, driver.find_element(By.XPATH, "//button[@type='submit' or contains(text(), 'Submit')]"))
    
    # 3. OTP
    WebDriverWait(driver, 15).until(lambda d: "otp" in d.current_url.lower())
    print("\n" + "="*50)
    print("OTP SENT! I am waiting right here!")
    print("PLEASE ENTER THE OTPS MANUALLY IN THE POPPED UP BROWSER WINDOW.")
    print("="*50 + "\n")
    
    # WAIT FOR HUMAN OTP COMPLETION
    # Once human submits, page goes to personal
    WebDriverWait(driver, 300).until(lambda d: "personal" in d.current_url.lower())
    print("\nOTP Validated by user! Resuming automation explicitly to scrape everything else...\n")
    
    # 4. Personal Information
    time.sleep(1)
    scrape_current_page(driver, "Personal Information")
    driver.execute_script("$('#personalinformationform-social_category').val(2).trigger('chosen:updated').change();")
    driver.execute_script("$('#personalinformationform-study_medium').val(2).trigger('chosen:updated').change();")
    driver.execute_script("document.querySelector('form').submit();")
    
    # 5. Address Details
    WebDriverWait(driver, 10).until(lambda d: "address" in d.current_url.lower())
    time.sleep(1)
    scrape_current_page(driver, "Address Details")
    js_type(driver, driver.find_element(By.ID, "addressdetailsform-permanent_address1"), "Test Address 123")
    js_type(driver, driver.find_element(By.ID, "addressdetailsform-permanent_pincode"), "110034")
    driver.execute_script("document.querySelector('form').submit();")
    
    # 6. Eligibility (If it appears here)
    time.sleep(2)
    current_url = driver.current_url.lower()
    if "eligibility" in current_url:
        scrape_current_page(driver, "Eligibility Details")
        driver.execute_script("document.getElementById('eligibilityform-date_of_appointment').value = '10-10-2022';")
        driver.execute_script("document.querySelector('form').submit();")
        time.sleep(2)
        current_url = driver.current_url.lower()
        
    # 7. Subject
    if "subject" in current_url:
        scrape_current_page(driver, "Subject Details")
        driver.execute_script("document.querySelector('form').submit();")
        time.sleep(2)
        current_url = driver.current_url.lower()
        
    # 8. Documents
    if "document" in current_url:
        scrape_current_page(driver, "Documents Upload")

    driver.quit()
    print("\nCOMPLETE! All pages scraped flawlessly.")
except Exception as e:
    os.environ["PATH"] = old_path
    print('Error:', str(e))
