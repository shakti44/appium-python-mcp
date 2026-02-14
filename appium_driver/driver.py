"""Appium driver wrapper with error recovery and utilities."""
from typing import Optional, List, Dict, Any, Union
from pathlib import Path
from datetime import datetime
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.logger import logger
from utils.helpers import retry
from config.environment import settings


class AppiumDriverWrapper:
    """Wrapper around Appium WebDriver with additional utilities."""
    
    def __init__(self, driver: webdriver.Remote):
        """
        Initialize driver wrapper.
        
        Args:
            driver: Appium WebDriver instance
        """
        self.driver = driver
        self.implicit_wait = settings.implicit_wait
        self.explicit_wait = settings.explicit_wait
        self.screenshot_dir = Path(settings.screenshot_dir)
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        # Set implicit wait
        self.driver.implicitly_wait(self.implicit_wait)
        
        logger.info(f"AppiumDriverWrapper initialized for {self.platform_name}")
    
    @property
    def platform_name(self) -> str:
        """Get platform name."""
        return self.driver.capabilities.get('platformName', 'Unknown')
    
    @property
    def device_name(self) -> str:
        """Get device name."""
        return self.driver.capabilities.get('deviceName', 'Unknown')
    
    def find_element(
        self,
        by: str,
        value: str,
        timeout: Optional[int] = None
    ):
        """
        Find element with explicit wait.
        
        Args:
            by: Locator strategy (e.g., AppiumBy.ID)
            value: Locator value
            timeout: Optional custom timeout
            
        Returns:
            WebElement
        """
        wait_time = timeout or self.explicit_wait
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((by, value))
            )
            logger.debug(f"Found element: {by}={value}")
            return element
        except TimeoutException:
            logger.error(f"Element not found: {by}={value} (timeout: {wait_time}s)")
            if settings.screenshot_on_failure:
                self.take_screenshot(f"element_not_found_{value}")
            raise NoSuchElementException(f"Element not found: {by}={value}")
    
    def find_elements(
        self,
        by: str,
        value: str,
        timeout: Optional[int] = None
    ) -> List:
        """
        Find multiple elements with explicit wait.
        
        Args:
            by: Locator strategy
            value: Locator value
            timeout: Optional custom timeout
            
        Returns:
            List of WebElements
        """
        wait_time = timeout or self.explicit_wait
        try:
            elements = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_all_elements_located((by, value))
            )
            logger.debug(f"Found {len(elements)} elements: {by}={value}")
            return elements
        except TimeoutException:
            logger.warning(f"No elements found: {by}={value}")
            return []
    
    @retry(max_attempts=3, delay=1.0)
    def click(self, by: str, value: str, timeout: Optional[int] = None):
        """
        Click element with retry.
        
        Args:
            by: Locator strategy
            value: Locator value
            timeout: Optional custom timeout
        """
        element = self.find_element(by, value, timeout)
        element.click()
        logger.info(f"Clicked element: {by}={value}")
    
    @retry(max_attempts=3, delay=1.0)
    def send_keys(
        self,
        by: str,
        value: str,
        text: str,
        clear_first: bool = True,
        timeout: Optional[int] = None
    ):
        """
        Send keys to element with retry.
        
        Args:
            by: Locator strategy
            value: Locator value
            text: Text to send
            clear_first: Clear field before typing
            timeout: Optional custom timeout
        """
        element = self.find_element(by, value, timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)
        logger.info(f"Sent keys to element: {by}={value}")
    
    def get_text(self, by: str, value: str, timeout: Optional[int] = None) -> str:
        """
        Get text from element.
        
        Args:
            by: Locator strategy
            value: Locator value
            timeout: Optional custom timeout
            
        Returns:
            Element text
        """
        element = self.find_element(by, value, timeout)
        text = element.text
        logger.debug(f"Got text from {by}={value}: {text}")
        return text
    
    def is_element_visible(
        self,
        by: str,
        value: str,
        timeout: Optional[int] = None
    ) -> bool:
        """
        Check if element is visible.
        
        Args:
            by: Locator strategy
            value: Locator value
            timeout: Optional custom timeout
            
        Returns:
            True if visible, False otherwise
        """
        wait_time = timeout or self.explicit_wait
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            return False
    
    def wait_for_element(
        self,
        by: str,
        value: str,
        timeout: Optional[int] = None
    ) -> bool:
        """
        Wait for element to be present.
        
        Args:
            by: Locator strategy
            value: Locator value
            timeout: Optional custom timeout
            
        Returns:
            True if found, False otherwise
        """
        try:
            self.find_element(by, value, timeout)
            return True
        except NoSuchElementException:
            return False
    
    def take_screenshot(self, name: Optional[str] = None) -> Path:
        """
        Take screenshot and save to file.
        
        Args:
            name: Optional screenshot name
            
        Returns:
            Path to screenshot file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png" if name else f"screenshot_{timestamp}.png"
        screenshot_path = self.screenshot_dir / filename
        
        self.driver.save_screenshot(str(screenshot_path))
        logger.info(f"Screenshot saved: {screenshot_path}")
        
        return screenshot_path
    
    def switch_to_context(self, context: str):
        """
        Switch to web or native context.
        
        Args:
            context: Context name (NATIVE_APP, WEBVIEW, etc.)
        """
        self.driver.switch_to.context(context)
        logger.info(f"Switched to context: {context}")
    
    def get_contexts(self) -> List[str]:
        """
        Get available contexts.
        
        Returns:
            List of context names
        """
        contexts = self.driver.contexts
        logger.debug(f"Available contexts: {contexts}")
        return contexts
    
    def get_current_context(self) -> str:
        """
        Get current context.
        
        Returns:
            Current context name
        """
        context = self.driver.current_context
        logger.debug(f"Current context: {context}")
        return context
    
    def scroll_to_element(
        self,
        by: str,
        value: str,
        max_scrolls: int = 10
    ):
        """
        Scroll until element is found.
        
        Args:
            by: Locator strategy
            value: Locator value
            max_scrolls: Maximum scroll attempts
            
        Returns:
            WebElement if found
        """
        for i in range(max_scrolls):
            try:
                return self.find_element(by, value, timeout=2)
            except NoSuchElementException:
                if self.platform_name.lower() == 'android':
                    self.driver.swipe(500, 1500, 500, 500, 500)
                else:
                    self.driver.execute_script('mobile: scroll', {'direction': 'down'})
        
        raise NoSuchElementException(f"Element not found after {max_scrolls} scrolls")
    
    def get_page_source(self) -> str:
        """
        Get page source XML.
        
        Returns:
            Page source as string
        """
        return self.driver.page_source
    
    def back(self):
        """Navigate back."""
        self.driver.back()
        logger.info("Navigated back")
    
    def close_app(self):
        """Close application."""
        self.driver.close_app()
        logger.info("Application closed")
    
    def launch_app(self):
        """Launch application."""
        self.driver.launch_app()
        logger.info("Application launched")
    
    def reset_app(self):
        """Reset application."""
        self.driver.reset()
        logger.info("Application reset")
    
    def install_app(self, app_path: str):
        """
        Install application.
        
        Args:
            app_path: Path to app file
        """
        self.driver.install_app(app_path)
        logger.info(f"Installed app: {app_path}")
    
    def remove_app(self, bundle_id: str):
        """
        Remove application.
        
        Args:
            bundle_id: App bundle ID or package name
        """
        self.driver.remove_app(bundle_id)
        logger.info(f"Removed app: {bundle_id}")
    
    def activate_app(self, bundle_id: str):
        """
        Activate (foreground) application.
        
        Args:
            bundle_id: App bundle ID or package name
        """
        self.driver.activate_app(bundle_id)
        logger.info(f"Activated app: {bundle_id}")
    
    def terminate_app(self, bundle_id: str):
        """
        Terminate application.
        
        Args:
            bundle_id: App bundle ID or package name
        """
        self.driver.terminate_app(bundle_id)
        logger.info(f"Terminated app: {bundle_id}")
    
    def get_device_time(self) -> str:
        """
        Get device time.
        
        Returns:
            Device time as string
        """
        return self.driver.device_time
    
    def get_battery_info(self) -> Dict[str, Any]:
        """
        Get battery information.
        
        Returns:
            Battery info dictionary
        """
        return self.driver.battery_info
    
    def set_network_connection(self, connection_type: int):
        """
        Set network connection type (Android only).
        
        Args:
            connection_type: Connection type (0=None, 1=Airplane, 2=WiFi, 4=Data, 6=All)
        """
        self.driver.set_network_connection(connection_type)
        logger.info(f"Set network connection: {connection_type}")
    
    def quit(self):
        """Quit driver."""
        self.driver.quit()
        logger.info("Driver quit")
