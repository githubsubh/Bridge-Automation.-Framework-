
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def check_admin():
    chrome_options = Options()
    # chrome_options.add_argument("--headless") # Comment out to see what's happening if needed
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        driver.get("https://bridge-uat-admin.nios.ac.in/auth/login")
        time.sleep(3)
        
        # Fill credentials
        driver.find_element(By.CSS_SELECTOR, "input[name*='username'], input[id*='email'], input[type='text']").send_keys("superadmin")
        driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys("Admin@2025")
        
        # Click login
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(5)
        
        print(f"Current URL: {driver.current_url}")
        
        # List all sidebar/menu links
        links = driver.find_elements(By.TAG_NAME, "a")
        print("\n--- Menu Links ---")
        for link in links:
            text = link.text.strip()
            if text:
                print(f"- {text}")
                
        # Specifically look for Masters or Exam
        masters = driver.find_elements(By.XPATH, "//*[contains(text(), 'Master')]")
        exam = driver.find_elements(By.XPATH, "//*[contains(text(), 'Exam')]")
        
        print(f"\nFound {len(masters)} elements with 'Master'")
        print(f"Found {len(exam)} elements with 'Exam'")
        
        # If possible, click on Master/Exam to see submenus
        for m in masters:
            print(f"Master element text: {m.text}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    check_admin()
