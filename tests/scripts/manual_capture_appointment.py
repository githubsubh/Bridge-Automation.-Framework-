from selenium import webdriver
from selenium.webdriver.common.by import By
from utilities.read_properties import ReadConfig
import time
import os

def capture_appointment_page():
    # Setup
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://bridge-uat.nios.ac.in/")
    
    email = ReadConfig.getLoginEmail()
    password = ReadConfig.getLoginPassword()

    print("=== MANUAL INTERVENTION REQUIRED ===")
    
    # 1. Login
    driver.find_element(By.XPATH, "//a[contains(text(),'Login Corner')]").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//a[contains(text(),'Teacher Login')]").click()
    
    print("1. Please complete Login (Email/Pass/Captcha)...")
    
    # Wait for login completion
    while "dashboard" not in driver.current_url:
        try:
            # Auto-fill if still on login page
            if "login" in driver.current_url:
                driver.find_element(By.ID, "loginform-email").send_keys(email)
                driver.find_element(By.ID, "loginform-password").send_keys(password)
                print("   (Auto-filled credentials, enter CAPTCHA now...)")
                time.sleep(15) # Wait for user
        except:
            pass
        time.sleep(2)

    print("Login Detected!")
    time.sleep(2)

    # 2. Navigate to Service
    print("Navigating to Change Appointment Date...")
    driver.get("https://bridge-uat.nios.ac.in/eservices/apply")
    time.sleep(3)
    
    # Click specific service
    # Assuming the link text or title. Since we don't have the exact locator handy, scraping the list
    links = driver.find_elements(By.CSS_SELECTOR, "li.list-group-item")
    target_url = None
    for link in links:
        if "Change Appointment Date" in link.text:
            target_url = link.find_element(By.TAG_NAME, "a").get_attribute("href")
            break
    
    if target_url:
        driver.get(target_url)
    else:
        print("Could not find service link! check manually.")
        return

    # 3. Wait for OTP
    print("2. Please Enter OTP and Verify...")
    while "verify-otp" in driver.current_url:
        time.sleep(2)
        
    print("OTP Page Passed! Capturing DOM...")
    time.sleep(3) # Wait for full load
    
    # 4. Capture
    dom_file = "eservice_appointment_dom.html"
    with open(dom_file, "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    
    print(f"DOM saved to {dom_file}")
    driver.quit()

if __name__ == "__main__":
    capture_appointment_page()
