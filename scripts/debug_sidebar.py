"""Debug script: Capture the admin portal post-login state to find correct sidebar locators."""
import time, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Use the same profile trick as conftest.py to avoid chromedriver mismatch
old_path = os.environ.get("PATH", "")
clean_paths = [p for p in old_path.split(";") if "Python313\\Scripts" not in p]
os.environ["PATH"] = ";".join(clean_paths)

options = Options()
options.add_argument("--start-maximized")
options.add_argument("--no-first-run")
options.add_argument("--no-default-browser-check")

driver = webdriver.Chrome(options=options)
os.environ["PATH"] = old_path  # Restore

try:
    # Step 1: Open admin portal
    driver.get("https://bridge-uat-admin.nios.ac.in")
    time.sleep(3)
    print(f"[1] URL after open: {driver.current_url}")
    print(f"[1] Title: {driver.title}")
    driver.save_screenshot("screenshots/debug_01_landing.png")

    # Step 2: Check for restricted access prompt
    password_fields = driver.find_elements(By.XPATH, "//input[@type='password' or @placeholder='Enter Access Password']")
    if password_fields and password_fields[0].is_displayed():
        print("[2] Restricted Access prompt FOUND. Entering password...")
        password_fields[0].send_keys("LetMeIn@2026")
        time.sleep(1)
        # Try to find and click submit
        btns = driver.find_elements(By.XPATH, "//button")
        print(f"[2] Found {len(btns)} buttons: {[b.text for b in btns]}")
        for btn in btns:
            if btn.text.strip():
                print(f"[2] Clicking button: '{btn.text}'")
                btn.click()
                break
        time.sleep(3)
        print(f"[2] URL after restricted access: {driver.current_url}")
        driver.save_screenshot("screenshots/debug_02_after_restricted.png")
    else:
        print("[2] No restricted access prompt found.")

    # Step 3: Login
    print(f"[3] Current URL before login: {driver.current_url}")
    username_fields = driver.find_elements(By.CSS_SELECTOR, "input[name*='username'], input[id*='email'], input[type='text']")
    password_fields = driver.find_elements(By.CSS_SELECTOR, "input[type='password']")
    print(f"[3] Username fields: {len(username_fields)}, Password fields: {len(password_fields)}")
    
    if username_fields and password_fields:
        username_fields[0].clear()
        username_fields[0].send_keys("Superadmin")
        password_fields[0].clear()
        password_fields[0].send_keys("Admin@2025")
        driver.save_screenshot("screenshots/debug_03_before_submit.png")
        
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()
        time.sleep(8)  # Long wait for dashboard
        
        print(f"[3] URL after login: {driver.current_url}")
        print(f"[3] Title after login: {driver.title}")
        driver.save_screenshot("screenshots/debug_04_after_login.png")
    
    # Step 4: Dump all links on the page
    all_links = driver.find_elements(By.TAG_NAME, "a")
    print(f"\n[4] === ALL LINKS ON PAGE ({len(all_links)} total) ===")
    for i, link in enumerate(all_links):
        text = link.text.strip()
        href = link.get_attribute("href") or ""
        if text:
            print(f"  [{i}] '{text}' -> {href}")
    
    # Step 5: Dump sidebar specifically
    sidebar_candidates = driver.find_elements(By.CSS_SELECTOR, ".sidebar, #sidebar, .nav-sidebar, .main-menu, nav, .left-sidebar, .metismenu, #left-sidebar")
    print(f"\n[5] === SIDEBAR ELEMENTS FOUND: {len(sidebar_candidates)} ===")
    for sc in sidebar_candidates:
        print(f"  Tag: {sc.tag_name}, Class: {sc.get_attribute('class')}, Text preview: {sc.text[:200]}")
    
    # Step 6: Check for error messages or alerts
    alerts = driver.find_elements(By.CSS_SELECTOR, ".alert, .error, .warning, .toast, .notification")
    print(f"\n[6] === ALERTS/ERRORS: {len(alerts)} ===")
    for a in alerts:
        print(f"  {a.text}")

    driver.save_screenshot("screenshots/debug_05_final.png")

except Exception as e:
    print(f"\nEXCEPTION: {e}")
    driver.save_screenshot("screenshots/debug_exception.png")
finally:
    driver.quit()
