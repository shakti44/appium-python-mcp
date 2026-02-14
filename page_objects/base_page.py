"""Base page object class for mobile automation."""
from typing import Optional, List, Any
from appium_driver.driver import AppiumDriverWrapper
from locators.strategy import Locator, LocatorBuilder
from locators.locator_engine import LocatorEngine
from actions.element_actions import ElementActions
from actions.device_actions import DeviceActions
from actions.gesture_actions import GestureActions
from utils.logger import logger
from utils.helpers import wait_until


class BasePage:
    """Base class for Page Object Model."""
    
    def __init__(self, driver_wrapper: AppiumDriverWrapper):
        """
        Initialize base page.
        
        Args:
            driver_wrapper: Appium driver wrapper instance
        """
        self.driver_wrapper = driver_wrapper
        self.driver = driver_wrapper.driver
        self.locator_engine = LocatorEngine(driver_wrapper)
        
        # Action instances
        self.element_actions = ElementActions(driver_wrapper)
        self.device_actions = DeviceActions(driver_wrapper)
        self.gesture_actions = GestureActions(driver_wrapper)
        
        self.logger = logger
    
    @property
    def platform(self) -> str:
        """Get platform name."""
        return self.driver_wrapper.platform_name
    
    @property
    def is_android(self) -> bool:
        """Check if platform is Android."""
        return self.platform.lower() == 'android'
    
    @property
    def is_ios(self) -> bool:
        """Check if platform is iOS."""
        return self.platform.lower() == 'ios'
    
    def find_element(
        self,
        locators: List[Locator],
        timeout: Optional[int] = None
    ) -> Any:
        """
        Find element with fallback.
        
        Args:
            locators: List of locators to try
            timeout: Optional custom timeout
            
        Returns:
            WebElement
        """
        return self.locator_engine.find_element_with_fallback(locators, timeout)
    
    def find_elements(
        self,
        locators: List[Locator],
        timeout: Optional[int] = None
    ) -> List[Any]:
        """
        Find multiple elements with fallback.
        
        Args:
            locators: List of locators to try
            timeout: Optional custom timeout
            
        Returns:
            List of WebElements
        """
        return self.locator_engine.find_elements_with_fallback(locators, timeout)
    
    def click(self, locators: List[Locator], timeout: Optional[int] = None):
        """
        Click an element.
        
        Args:
            locators: List of locators to try
            timeout: Optional custom timeout
            
        Returns:
            Self for method chaining
        """
        self.element_actions.click(locators, timeout)
        return self
    
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
            
        Returns:
            Self for method chaining
        """
        self.element_actions.send_keys(locators, text, clear_first, timeout)
        return self
    
    def get_text(
        self,
        locators: List[Locator],
        timeout: Optional[int] = None
    ) -> str:
        """
        Get text from element.
        
        Args:
            locators: List of locators to try
            timeout: Optional custom timeout
            
        Returns:
            Element text
        """
        return self.element_actions.get_text(locators, timeout)
    
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
        return self.element_actions.is_displayed(locators, timeout)
    
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
        return self.element_actions.wait_for_element(locators, timeout)
    
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
        return self.element_actions.wait_for_element_to_disappear(locators, timeout)
    
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
            Self for method chaining
        """
        self.element_actions.scroll_to_element(locators, max_scrolls)
        return self
    
    def swipe_left(self, duration: int = 500):
        """
        Swipe left.
        
        Args:
            duration: Swipe duration in milliseconds
            
        Returns:
            Self for method chaining
        """
        self.gesture_actions.swipe_left(duration)
        return self
    
    def swipe_right(self, duration: int = 500):
        """
        Swipe right.
        
        Args:
            duration: Swipe duration in milliseconds
            
        Returns:
            Self for method chaining
        """
        self.gesture_actions.swipe_right(duration)
        return self
    
    def swipe_up(self, duration: int = 500):
        """
        Swipe up.
        
        Args:
            duration: Swipe duration in milliseconds
            
        Returns:
            Self for method chaining
        """
        self.gesture_actions.swipe_up(duration)
        return self
    
    def swipe_down(self, duration: int = 500):
        """
        Swipe down.
        
        Args:
            duration: Swipe duration in milliseconds
            
        Returns:
            Self for method chaining
        """
        self.gesture_actions.swipe_down(duration)
        return self
    
    def back(self):
        """
        Navigate back.
        
        Returns:
            Self for method chaining
        """
        self.device_actions.back()
        return self
    
    def hide_keyboard(self):
        """
        Hide keyboard.
        
        Returns:
            Self for method chaining
        """
        self.device_actions.hide_keyboard()
        return self
    
    def take_screenshot(self, name: Optional[str] = None):
        """
        Take screenshot.
        
        Args:
            name: Optional screenshot name
            
        Returns:
            Path to screenshot
        """
        return self.device_actions.take_screenshot(name)
    
    def wait_until(
        self,
        condition,
        timeout: float = 10.0,
        error_message: Optional[str] = None
    ) -> bool:
        """
        Wait until condition is true.
        
        Args:
            condition: Callable that returns boolean
            timeout: Maximum time to wait
            error_message: Optional error message
            
        Returns:
            True if condition met
        """
        return wait_until(condition, timeout, error_message=error_message)
    
    def create_locator_builder(self) -> LocatorBuilder:
        """
        Create a new locator builder.
        
        Returns:
            LocatorBuilder instance
        """
        return LocatorBuilder()
