import pytest
import time
from utilities.custom_logger import LogGen

class Test_FindBrowser:
    logger = LogGen.loggen()
    
    def test_open_and_stay(self, setup):
        """Opens Chrome and stays open for 60 seconds so you can find it"""
        self.driver = setup
        
        # Make window HUGE and on top
        self.driver.maximize_window()
        self.driver.set_window_position(0, 0)
        
        # Navigate to bright red page
        self.driver.get("data:text/html,<html><body style='background-color:red; font-size:72px; text-align:center; padding:100px;'><h1>🔴 CHROME IS OPEN HERE! 🔴</h1><p>If you see this - you found Chrome!</p><p>This window will stay open for 60 seconds</p></body></html>")
        
        print("\n" + "="*60)
        print("🔴 CHROME BROWSER IS NOW OPEN!")
        print("🔍 Look for a BRIGHT RED WINDOW")
        print("📍 Check ALL your desktops/workspaces (F3 or Mission Control)")
        print("⏰ Window will stay open for 60 seconds")
        print("="*60 + "\n")
        
        # Keep browser open for 60 seconds
        for i in range(60, 0, -1):
            self.driver.execute_script(f"document.title = '🔴 FIND ME! - {i} seconds remaining';")
            time.sleep(1)
            
        print("\n✅ Test Complete - Browser will close now\n")
