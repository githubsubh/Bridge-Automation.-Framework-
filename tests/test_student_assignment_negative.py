import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# Create dummy files for testing
def setup_test_files():
    with open('test_malicious.exe', 'w') as f: f.write('fake exe')
    with open('test_empty.pdf', 'wb') as f: pass
    with open('test_fake.pdf', 'w') as f: f.write('not a real pdf content')
    with open('test_special_#@%.pdf', 'w') as f: f.write('special chars')

def run_negative_tests():
    setup_test_files()
    cwd = os.getcwd()
    
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(10)
    
    try:
        # 1. Login
        driver.get("https://bridge-uat.nios.ac.in/auth/login")
        driver.find_element(By.NAME, "LoginForm[username]").send_keys("subh7409@gmail.com")
        driver.find_element(By.NAME, "LoginForm[password]").send_keys("Password@12")
        
        print("LOGIN: Please enter captcha manually and click Login...")
        # Wait for redirect to dashboard
        WebDriverWait(driver, 120).until(EC.url_contains("dashboard"))
        
        # 2. Navigate to Assignment Module
        # We find the Math subject (501)
        driver.get("https://bridge-uat.nios.ac.in/teacher/dashboard")
        time.sleep(2)
        
        # Click on Assignments (based on dashboard_page.py patterns)
        # For now, navigate directly to Mathematics upload if we have the URL or find the button
        # Assuming the URL from previous turn
        upload_url = "https://bridge-uat.nios.ac.in/assignment/upload/d468b896-01ab-11ec-b03d-025c3e693150"
        driver.get(upload_url)
        time.sleep(3)
        
        # TEST CASES
        test_files = [
            ('test_malicious.exe', 'TC_STU_19: Unsupported Extension'),
            ('test_empty.pdf', 'TC_STU_21: Empty 0KB File'),
            ('test_fake.pdf', 'TC_STU_20: Corrupted Content (Text as PDF)'),
            ('test_special_#@%.pdf', 'TC_STU_22: Special Chars in Name')
        ]
        
        for filename, tc_id in test_files:
            print(f"\n--- Running {tc_id} ---")
            driver.refresh()
            time.sleep(2)
            
            # Find the file input (often nested in an accordion)
            # Find all file inputs if multiple subjects, but we are on a specific upload page
            file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            
            file_path = os.path.join(cwd, filename)
            file_input.send_keys(file_path)
            time.sleep(1)
            
            # Click the specific Submit button for the assignment
            # Search for the button text "Final Submit" or "Submit Assignment"
            submit_btns = driver.find_elements(By.TAG_NAME, "button")
            target_btn = None
            for btn in submit_btns:
                if "Submit" in btn.text or "Upload" in btn.text:
                    target_btn = btn
                    break
            
            if target_btn:
                target_btn.click()
                print(f"Clicked Submit for {filename}")
                time.sleep(3)
                # Capture any error message on page
                body_text = driver.find_element(By.TAG_NAME, "body").text
                if "Only PDF files" in body_text or "error" in body_text.lower() or "invalid" in body_text.lower():
                    print(f"RESULT: System correctly handled/blocked {filename}")
                else:
                    print(f"RESULT: Potential Leak! System might have accepted {filename}")
            else:
                print("Could not find Submit button!")

    finally:
        driver.quit()

if __name__ == "__main__":
    run_negative_tests()
