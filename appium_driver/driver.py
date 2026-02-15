"""Appium Driver Wrapper

This is an Appium driver wrapper for both Android and iOS platforms.
It simplifies the process of initializing the Appium driver and interacting with mobile applications.
"""

from appium import webdriver
from typing import Optional, Dict, Any


class AppiumDriver:
    """Appium driver wrapper for mobile automation"""
    
    def __init__(
        self, 
        platform_name: str,
        device_name: str,
        app: str,
        automation_name: str = 'UiAutomator2',
        appium_server_url: str = 'http://localhost:4723'
    ):
        """Initialize Appium driver with desired capabilities
        
        Args:
            platform_name: Platform name (Android/iOS)
            device_name: Name of the device
            app: Path to the app
            automation_name: Automation name (default: UiAutomator2)
            appium_server_url: Appium server URL (default: http://localhost:4723)
        """
        self.desired_caps = {
            'platformName': platform_name,
            'deviceName': device_name,
            'app': app,
            'automationName': automation_name
        }
        self.appium_server_url = appium_server_url
        self.driver: Optional[webdriver.Remote] = None
        
    def start(self):
        """Start the Appium driver session"""
        if self.driver is None:
            self.driver = webdriver.Remote(self.appium_server_url, self.desired_caps)
        return self.driver
    
    def quit(self):
        """Quit the Appium driver session"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def find_element(self, by: str, value: str):
        """Find an element on the screen
        
        Args:
            by: Locator strategy (e.g., 'id', 'xpath', 'accessibility id')
            value: Locator value
            
        Returns:
            WebElement if found
        """
        if not self.driver:
            raise RuntimeError("Driver not started. Call start() first.")
        return self.driver.find_element(by, value)
    
    def tap(self, x: int, y: int):
        """Tap at coordinates
        
        Args:
            x: X coordinate
            y: Y coordinate
        """
        if not self.driver:
            raise RuntimeError("Driver not started. Call start() first.")
        self.driver.tap([(x, y)])
    
    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: int = 1000):
        """Swipe from one point to another
        
        Args:
            start_x: Starting X coordinate
            start_y: Starting Y coordinate
            end_x: Ending X coordinate
            end_y: Ending Y coordinate
            duration: Duration in milliseconds (default: 1000)
        """
        if not self.driver:
            raise RuntimeError("Driver not started. Call start() first.")
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)
    
    def get_page_source(self) -> str:
        """Get the page source
        
        Returns:
            Page source as string
        """
        if not self.driver:
            raise RuntimeError("Driver not started. Call start() first.")
        return self.driver.page_source
    
    def screenshot(self, filename: str):
        """Take a screenshot
        
        Args:
            filename: Path to save screenshot
        """
        if not self.driver:
            raise RuntimeError("Driver not started. Call start() first.")
        self.driver.save_screenshot(filename)
 
