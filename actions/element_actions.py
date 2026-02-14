"""Element-level actions for mobile automation."""
from typing import Optional, List
from actions.base_actions import BaseActions
from locators.strategy import Locator
from locators.locator_engine import LocatorEngine


class ElementActions(BaseActions):
    """Actions for interacting with elements."""
    
    def __init__(self, driver_wrapper):
        """Initialize element actions."""
        super().__init__(driver_wrapper)
        self.locator_engine = LocatorEngine(driver_wrapper)
    
    def click(
        self,
        locators: List[Locator],
        timeout: Optional[int] = None
    ):
        """
        Click an element.
        
        Args:
            locators: List of locators to try
            timeout: Optional custom timeout
        """
        element = self.locator_engine.find_element_with_fallback(locators, timeout)
        element.click()
        self.logger.info("Element clicked")
    
    def send_keys(
        self,
        locators: List[Locator],
        text: str,
        clear_first: bool = True,
        timeout: Optional[int] = None
    ):
        """
        Send keys to an element.
        
        Args:
            locators: List of locators to try
            text: Text to send
            clear_first: Whether to clear field first
            timeout: Optional custom timeout
        """
        element = self.locator_engine.find_element_with_fallback(locators, timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)
        self.logger.info(f"Sent keys: {text}")
    
    def get_text(
        self,
        locators: List[Locator],
        timeout: Optional[int] = None
    ) -> str:
        """
        Get text from an element.
        
        Args:
            locators: List of locators to try
            timeout: Optional custom timeout
            
        Returns:
            Element text
        """
        element = self.locator_engine.find_element_with_fallback(locators, timeout)
        text = element.text
        self.logger.info(f"Got text: {text}")
        return text
    
    def get_attribute(
        self,
        locators: List[Locator],
        attribute: str,
        timeout: Optional[int] = None
    ) -> str:
        """
        Get attribute value from an element.
        
        Args:
            locators: List of locators to try
            attribute: Attribute name
            timeout: Optional custom timeout
            
        Returns:
            Attribute value
        """
        element = self.locator_engine.find_element_with_fallback(locators, timeout)
        value = element.get_attribute(attribute)
        self.logger.info(f"Got attribute {attribute}: {value}")
        return value
    
    def is_displayed(
        self,
        locators: List[Locator],
        timeout: Optional[int] = None
    ) -> bool:
        """
        Check if element is displayed.
        
        Args:
            locators: List of locators to try
            timeout: Optional custom timeout
            
        Returns:
            True if displayed, False otherwise
        """
        try:
            element = self.locator_engine.find_element_with_fallback(locators, timeout)
            return element.is_displayed()
        except Exception:
            return False
    
    def is_enabled(
        self,
        locators: List[Locator],
        timeout: Optional[int] = None
    ) -> bool:
        """
        Check if element is enabled.
        
        Args:
            locators: List of locators to try
            timeout: Optional custom timeout
            
        Returns:
            True if enabled, False otherwise
        """
        try:
            element = self.locator_engine.find_element_with_fallback(locators, timeout)
            return element.is_enabled()
        except Exception:
            return False
    
    def is_selected(
        self,
        locators: List[Locator],
        timeout: Optional[int] = None
    ) -> bool:
        """
        Check if element is selected (checkbox/radio).
        
        Args:
            locators: List of locators to try
            timeout: Optional custom timeout
            
        Returns:
            True if selected, False otherwise
        """
        try:
            element = self.locator_engine.find_element_with_fallback(locators, timeout)
            return element.is_selected()
        except Exception:
            return False
    
    def wait_for_element(
        self,
        locators: List[Locator],
        timeout: Optional[int] = None
    ) -> bool:
        """
        Wait for element to appear.
        
        Args:
            locators: List of locators to try
            timeout: Optional custom timeout
            
        Returns:
            True if element appears, False otherwise
        """
        return self.locator_engine.wait_for_element(locators, timeout)
    
    def wait_for_element_to_disappear(
        self,
        locators: List[Locator],
        timeout: Optional[int] = None
    ) -> bool:
        """
        Wait for element to disappear.
        
        Args:
            locators: List of locators to try
            timeout: Optional custom timeout
            
        Returns:
            True if element disappears, False otherwise
        """
        import time
        start_time = time.time()
        timeout = timeout or self.driver_wrapper.explicit_wait
        
        while time.time() - start_time < timeout:
            if not self.locator_engine.is_element_present(locators, timeout=1):
                return True
            time.sleep(0.5)
        
        return False
    
    def get_location(
        self,
        locators: List[Locator],
        timeout: Optional[int] = None
    ) -> dict:
        """
        Get element location.
        
        Args:
            locators: List of locators to try
            timeout: Optional custom timeout
            
        Returns:
            Dictionary with x, y coordinates
        """
        element = self.locator_engine.find_element_with_fallback(locators, timeout)
        return element.location
    
    def get_size(
        self,
        locators: List[Locator],
        timeout: Optional[int] = None
    ) -> dict:
        """
        Get element size.
        
        Args:
            locators: List of locators to try
            timeout: Optional custom timeout
            
        Returns:
            Dictionary with width, height
        """
        element = self.locator_engine.find_element_with_fallback(locators, timeout)
        return element.size
    
    def scroll_to_element(
        self,
        locators: List[Locator],
        max_scrolls: int = 10
    ):
        """
        Scroll until element is found.
        
        Args:
            locators: List of locators to try
            max_scrolls: Maximum scroll attempts
            
        Returns:
            WebElement if found
        """
        for i in range(max_scrolls):
            if self.locator_engine.is_element_present(locators, timeout=2):
                return self.locator_engine.find_element_with_fallback(locators)
            
            # Perform scroll
            if self.driver_wrapper.platform_name.lower() == 'android':
                self.driver.swipe(500, 1500, 500, 500, 500)
            else:
                self.driver.execute_script('mobile: scroll', {'direction': 'down'})
        
        raise Exception(f"Element not found after {max_scrolls} scrolls")
    
    def long_press(
        self,
        locators: List[Locator],
        duration: int = 1000,
        timeout: Optional[int] = None
    ):
        """
        Long press on an element.
        
        Args:
            locators: List of locators to try
            duration: Press duration in milliseconds
            timeout: Optional custom timeout
        """
        from appium.webdriver.common.touch_action import TouchAction
        
        element = self.locator_engine.find_element_with_fallback(locators, timeout)
        action = TouchAction(self.driver)
        action.long_press(element, duration=duration).release().perform()
        self.logger.info(f"Long pressed element for {duration}ms")
    
    def get_available_actions(self) -> list[str]:
        """Get list of available actions."""
        return [
            'click', 'send_keys', 'get_text', 'get_attribute',
            'is_displayed', 'is_enabled', 'is_selected',
            'wait_for_element', 'wait_for_element_to_disappear',
            'get_location', 'get_size', 'scroll_to_element', 'long_press'
        ]
