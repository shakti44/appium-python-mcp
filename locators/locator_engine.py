"""Intelligent locator engine with multi-strategy fallback."""
from typing import Optional, List, Any
from appium_driver.driver import AppiumDriverWrapper
from locators.strategy import Locator, LocatorMapper, LocatorBuilder
from selenium.common.exceptions import NoSuchElementException
from utils.logger import logger


class LocatorEngine:
    """Engine for finding elements with intelligent fallback."""
    
    def __init__(self, driver_wrapper: AppiumDriverWrapper):
        """
        Initialize locator engine.
        
        Args:
            driver_wrapper: Appium driver wrapper instance
        """
        self.driver_wrapper = driver_wrapper
        self.driver = driver_wrapper.driver
    
    def find_element_with_fallback(
        self,
        locators: List[Locator],
        timeout: Optional[int] = None
    ) -> Any:
        """
        Find element using multiple locator strategies with fallback.
        
        Args:
            locators: List of locators to try
            timeout: Optional custom timeout per locator
            
        Returns:
            WebElement
            
        Raises:
            NoSuchElementException: If element not found with any locator
        """
        errors = []
        
        for locator in locators:
            try:
                logger.debug(f"Trying locator: {locator}")
                by = LocatorMapper.get_appium_by(locator.strategy)
                element = self.driver_wrapper.find_element(by, locator.value, timeout)
                logger.info(f"Element found using: {locator}")
                return element
            except NoSuchElementException as e:
                error_msg = f"{locator}: {str(e)}"
                errors.append(error_msg)
                logger.debug(f"Locator failed: {error_msg}")
                continue
        
        # If all locators failed
        error_summary = "\n".join(errors)
        logger.error(f"All locators failed:\n{error_summary}")
        raise NoSuchElementException(f"Element not found with any locator. Tried:\n{error_summary}")
    
    def find_elements_with_fallback(
        self,
        locators: List[Locator],
        timeout: Optional[int] = None
    ) -> List[Any]:
        """
        Find multiple elements using locator strategies with fallback.
        
        Args:
            locators: List of locators to try
            timeout: Optional custom timeout per locator
            
        Returns:
            List of WebElements
        """
        for locator in locators:
            try:
                logger.debug(f"Trying locator: {locator}")
                by = LocatorMapper.get_appium_by(locator.strategy)
                elements = self.driver_wrapper.find_elements(by, locator.value, timeout)
                if elements:
                    logger.info(f"Found {len(elements)} elements using: {locator}")
                    return elements
            except Exception as e:
                logger.debug(f"Locator failed: {locator} - {e}")
                continue
        
        logger.warning("No elements found with any locator")
        return []
    
    def is_element_present(
        self,
        locators: List[Locator],
        timeout: Optional[int] = 2
    ) -> bool:
        """
        Check if element is present using any locator.
        
        Args:
            locators: List of locators to try
            timeout: Timeout per locator (short default)
            
        Returns:
            True if element found, False otherwise
        """
        try:
            self.find_element_with_fallback(locators, timeout)
            return True
        except NoSuchElementException:
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
        try:
            self.find_element_with_fallback(locators, timeout)
            return True
        except NoSuchElementException:
            return False
    
    def create_smart_locator(
        self,
        text: Optional[str] = None,
        resource_id: Optional[str] = None,
        class_name: Optional[str] = None,
        accessibility_id: Optional[str] = None,
        xpath: Optional[str] = None,
        platform: Optional[str] = None
    ) -> List[Locator]:
        """
        Create smart locators with automatic fallback strategy.
        
        Args:
            text: Element text
            resource_id: Android resource ID or iOS element ID
            class_name: Element class name
            accessibility_id: Accessibility identifier
            xpath: XPath expression
            platform: Platform name (Android/iOS)
            
        Returns:
            List of locators with intelligent priority
        """
        builder = LocatorBuilder()
        
        # Accessibility ID gets highest priority
        if accessibility_id:
            builder.add_accessibility_id(accessibility_id, priority=10)
        
        # Platform-specific IDs
        if resource_id:
            if platform and platform.lower() == 'android':
                # Android resource-id
                builder.add_id(resource_id, priority=15)
                builder.add_android_uiautomator(
                    f'new UiSelector().resourceId("{resource_id}")',
                    priority=20
                )
            else:
                # iOS or generic ID
                builder.add_id(resource_id, priority=15)
        
        # Text-based locators
        if text:
            if platform and platform.lower() == 'android':
                builder.add_android_uiautomator(
                    f'new UiSelector().text("{text}")',
                    priority=30
                )
                builder.add_android_uiautomator(
                    f'new UiSelector().textContains("{text}")',
                    priority=35
                )
            elif platform and platform.lower() == 'ios':
                builder.add_ios_predicate(
                    f'label == "{text}" OR name == "{text}"',
                    priority=30
                )
                builder.add_ios_class_chain(
                    f'**/XCUIElementTypeAny[`label == "{text}"`]',
                    priority=35
                )
        
        # Class name
        if class_name:
            builder.add_class_name(class_name, priority=50)
        
        # XPath as last resort
        if xpath:
            builder.add_xpath(xpath, priority=100)
        
        # If text but no XPath, create generic XPath
        elif text:
            builder.add_xpath(f'//*[@text="{text}"]', priority=100)
            builder.add_xpath(f'//*[contains(@text, "{text}")]', priority=110)
        
        return builder.build()
