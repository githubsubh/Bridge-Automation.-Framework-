import pytest
import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.registration_page import RegistrationPage
from pages.authentication_page import AuthenticationPage
from pages.personal_information_page import PersonalInformationPage
from pages.address_details_page import AddressDetailsPage
from pages.subject_details_page import SubjectDetailsPage
from pages.documents_page import DocumentsPage
from utilities.read_properties import ReadConfig

def extract_dom_limits(driver, page_name):
    print(f"\n--- Extracting {page_name} ---")
    data = []
    inputs = driver.find_elements(By.TAG_NAME, 'input')
    selects = driver.find_elements(By.TAG_NAME, 'select')
    for el in inputs + selects:
        try:
            val_id = el.get_attribute('id') or ''
            val_name = el.get_attribute('name') or ''
            if not val_id and not val_name: continue
            
            data.append({
                'page': page_name,
                'id': val_id,
                'type': el.get_attribute('type') or '',
                'maxlength': el.get_attribute('maxlength') or '',
                'minlength': el.get_attribute('minlength') or '',
                'pattern': el.get_attribute('pattern') or '',
                'class': el.get_attribute('class') or ''
            })
        except: pass
    
    with open("DOM_EXTRACTIONS.txt", "a") as f:
        for item in data:
            f.write(json.dumps(item) + "\n")
    print(f"Extraction for {page_name} complete.")

def test_scrape_all_pages(setup):
    driver = setup
    baseURL = ReadConfig.getApplicationURL()
    driver.get(baseURL)
    
    with open("DOM_EXTRACTIONS.txt", "w") as f: f.write("")
    
    reg_page = RegistrationPage(driver)
    reg_page.handle_modal()
    reg_page.wait_for_form()
    
    print("\nExtracting Basic Details...")
    extract_dom_limits(driver, "Basic Details")
    
    # Fill only fields we know exist on UAT
    driver.execute_script("document.getElementById('basicdetailform-name').value = 'TEST SCRAPER'; document.getElementById('basicdetailform-name').dispatchEvent(new Event('input'));")
    driver.execute_script("document.getElementById('basicdetailform-date_of_birth').value = '10-10-1990'; document.getElementById('basicdetailform-date_of_birth').dispatchEvent(new Event('input'));")
    
    driver.find_element(By.ID, "basicdetailform_gender_chosen").click()
    time.sleep(0.5)
    driver.find_element(By.XPATH, "//div[@id='basicdetailform_gender_chosen']//li[contains(text(), 'Male')]").click()
    
    try: driver.execute_script("document.getElementById('basicdetailform-pan').value = 'ABCDE1234F';")
    except: pass
    try: driver.execute_script("document.getElementById('basicdetailform-aadhaar_no').value = '987654321012';")
    except: pass
    
    try: driver.execute_script("document.querySelector('button[type=submit]').click();")
    except: pass
    time.sleep(2)
    
    # Bypass unexpected "Are you sure" modal if it exists
    try:
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.swal2-actions button.swal2-confirm"))).click()
        time.sleep(1)
    except: pass

    # Auth
    WebDriverWait(driver, 15).until(lambda d: "authentication" in d.current_url.lower())
    extract_dom_limits(driver, "Authentication")
    driver.execute_script("document.getElementById('authenticationform-email').value = 'subh7409+740@gmail.com';")
    driver.execute_script("document.getElementById('authenticationform-mobile_no').value = '8287461243';")
    driver.execute_script("document.querySelector('button[type=submit]').click();")
    
    WebDriverWait(driver, 15).until(lambda d: "otp" in d.current_url.lower())
    extract_dom_limits(driver, "OTP")
    
    print("="*50)
    print("ACTION REQUIRED: ENTER THE OTP IN THE OPEN BROWSER WINODW NOW!")
    print("="*50)
    
    WebDriverWait(driver, 300).until(lambda d: "personal" in d.current_url.lower() or "address" in d.current_url.lower())
    
    # ------------------
    # Personal Info
    # ------------------
    if "personal" in driver.current_url.lower():
        extract_dom_limits(driver, "Personal Info")
        time.sleep(1)
        try: driver.execute_script("$('#personalinformationform-social_category').val(2).trigger('chosen:updated').change();")
        except: pass
        try: driver.execute_script("$('#personalinformationform-study_medium').val(2).trigger('chosen:updated').change();")
        except: pass
        driver.execute_script("document.querySelector('form').submit();")
    
    # ------------------
    # Address
    # ------------------
    WebDriverWait(driver, 10).until(lambda d: "address" in d.current_url.lower())
    extract_dom_limits(driver, "Address")
    driver.execute_script("document.getElementById('addressdetailsform-permanent_address1').value = 'Sample Address';")
    driver.execute_script("document.getElementById('addressdetailsform-permanent_pincode').value = '110034';")
    try:
        driver.execute_script("$('#addressdetailsform-permanent_state').val('DELHI').change();")
        time.sleep(1)
        driver.execute_script("$('#addressdetailsform-permanent_district').val('CENTRAL').change();")
    except: pass
    driver.execute_script("document.querySelector('form').submit();")

    # ------------------
    # Eligibility & Subject
    # ------------------
    try:
        WebDriverWait(driver, 5).until(lambda d: "eligibility" in d.current_url.lower() or "subject" in d.current_url.lower() or "document" in d.current_url.lower())
        if "eligibility" in driver.current_url.lower():
            extract_dom_limits(driver, "Eligibility Details")
            driver.execute_script("document.getElementById('eligibilityform-date_of_appointment').value = '10-10-2022';")
            driver.execute_script("document.querySelector('form').submit();")
            WebDriverWait(driver, 5).until(lambda d: "subject" in d.current_url.lower() or "document" in d.current_url.lower())
            
        if "subject" in driver.current_url.lower():
            extract_dom_limits(driver, "Subjects")
            driver.execute_script("document.querySelector('form').submit();")
            WebDriverWait(driver, 5).until(lambda d: "document" in d.current_url.lower())
    except: pass

    # ------------------
    # Documents
    # ------------------
    if "document" in driver.current_url.lower():
        extract_dom_limits(driver, "Documents")

    print("\nALL PAGES EXTRACTED SUCCESSFULLY!")
    time.sleep(10)
