import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def test_init():
    driver_path = r"C:\Users\Insph\.wdm\drivers\chromedriver\win64\144.0.7559.133\chromedriver-win32\chromedriver.exe"
    print(f"Testing with Driver: {driver_path}")
    print(f"Exists: {os.path.exists(driver_path)}")

    options = Options()
    # options.add_argument("--headless")
    
    try:
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        print("SUCCESS! Browser launched.")
        driver.quit()
    except Exception as e:
        print(f"FAILURE: {e}")

if __name__ == "__main__":
    test_init()
