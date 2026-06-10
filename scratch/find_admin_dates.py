
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

def run():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        driver.get("https://bridge-uat-admin.nios.ac.in/auth/login")
        time.sleep(3)
        
        # Restricted Access check
        try:
            pwd_field = driver.find_elements(By.XPATH, "//input[@type='password' or @placeholder='Enter Access Password']")
            if pwd_field and pwd_field[0].is_displayed():
                pwd_field[0].send_keys("LetMeIn@2026")
                submit = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit') or contains(text(), 'Verify')]")
                driver.execute_script("arguments[0].click();", submit)
                time.sleep(3)
        except: pass

        # Login
        driver.find_element(By.ID, "loginform-username").send_keys("superadmin")
        driver.find_element(By.ID, "loginform-password").send_keys("Admin@2025")
        
        # Captcha might be here. If so, I'll try to read it if it's easy, or just fail.
        # But wait, I can't read it easily. 
        # Let's see if I can find any text that says 'Exam'
        
        login_btn = driver.find_element(By.NAME, "login-button")
        driver.execute_script("arguments[0].click();", login_btn)
        time.sleep(10)
        
        print(f"URL: {driver.current_url}")
        driver.save_screenshot("scratch/admin_final.png")
        
        # List all menu items
        menu_items = driver.find_elements(By.TAG_NAME, "a")
        for item in menu_items:
            t = item.text.strip()
            if t:
                print(f"Menu: {t}")
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run()
