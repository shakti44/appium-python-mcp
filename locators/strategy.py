"""Locator strategies for element finding."""
from enum import Enum
from typing import Dict, Any, Optional, Callable
from appium.webdriver.common.appiumby import AppiumBy


class LocatorStrategy(str, Enum):
    """Supported locator strategies."""
    ACCESSIBILITY_ID = "accessibility_id"
    ID = "id"
    XPATH = "xpath"
    CLASS_NAME = "class_name"
    IOS_PREDICATE = "ios_predicate"
    IOS_CLASS_CHAIN = "ios_class_chain"
    ANDROID_UIAUTOMATOR = "android_uiautomator"
    ANDROID_VIEWTAG = "android_viewtag"
    NAME = "name"
    TAG_NAME = "tag_name"
    LINK_TEXT = "link_text"
    PARTIAL_LINK_TEXT = "partial_link_text"
    CSS_SELECTOR = "css_selector"


class LocatorMapper:
    """Maps locator strategies to Appium By strategies."""
    
    STRATEGY_MAP = {
        LocatorStrategy.ACCESSIBILITY_ID: AppiumBy.ACCESSIBILITY_ID,
        LocatorStrategy.ID: AppiumBy.ID,
        LocatorStrategy.XPATH: AppiumBy.XPATH,
        LocatorStrategy.CLASS_NAME: AppiumBy.CLASS_NAME,
        LocatorStrategy.IOS_PREDICATE: AppiumBy.IOS_PREDICATE,
        LocatorStrategy.IOS_CLASS_CHAIN: AppiumBy.IOS_CLASS_CHAIN,
        LocatorStrategy.ANDROID_UIAUTOMATOR: AppiumBy.ANDROID_UIAUTOMATOR,
        LocatorStrategy.ANDROID_VIEWTAG: AppiumBy.ANDROID_VIEWTAG,
        LocatorStrategy.NAME: AppiumBy.NAME,
        LocatorStrategy.TAG_NAME: AppiumBy.TAG_NAME,
        LocatorStrategy.LINK_TEXT: AppiumBy.LINK_TEXT,
        LocatorStrategy.PARTIAL_LINK_TEXT: AppiumBy.PARTIAL_LINK_TEXT,
        LocatorStrategy.CSS_SELECTOR: AppiumBy.CSS_SELECTOR,
    }
    
    @classmethod
    def get_appium_by(cls, strategy: LocatorStrategy) -> str:
        """
        Get Appium By constant for strategy.
        
        Args:
            strategy: Locator strategy
            
        Returns:
            Appium By constant
        """
        return cls.STRATEGY_MAP.get(strategy, AppiumBy.XPATH)


class Locator:
    """Represents a locator with strategy and value."""
    
    def __init__(
        self,
        strategy: LocatorStrategy,
        value: str,
        description: Optional[str] = None,
        priority: int = 100
    ):
        """
        Initialize locator.
        
        Args:
            strategy: Locator strategy
            value: Locator value
            description: Human-readable description
            priority: Priority for fallback (lower is higher priority)
        """
        self.strategy = strategy
        self.value = value
        self.description = description or f"{strategy}={value}"
        self.priority = priority
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "strategy": self.strategy.value,
            "value": self.value,
            "description": self.description,
            "priority": self.priority
        }
    
    def __repr__(self) -> str:
        return f"Locator({self.strategy.value}='{self.value}')"


class LocatorBuilder:
    """Builder for creating locators with fallback strategies."""
    
    def __init__(self):
        """Initialize locator builder."""
        self._locators: list[Locator] = []
    
    def add_accessibility_id(
        self,
        value: str,
        priority: int = 10,
        description: Optional[str] = None
    ) -> 'LocatorBuilder':
        """Add accessibility ID locator (highest priority by default)."""
        locator = Locator(
            LocatorStrategy.ACCESSIBILITY_ID,
            value,
            description,
            priority
        )
        self._locators.append(locator)
        return self
    
    def add_id(
        self,
        value: str,
        priority: int = 20,
        description: Optional[str] = None
    ) -> 'LocatorBuilder':
        """Add ID locator."""
        locator = Locator(
            LocatorStrategy.ID,
            value,
            description,
            priority
        )
        self._locators.append(locator)
        return self
    
    def add_xpath(
        self,
        value: str,
        priority: int = 100,
        description: Optional[str] = None
    ) -> 'LocatorBuilder':
        """Add XPath locator (low priority by default)."""
        locator = Locator(
            LocatorStrategy.XPATH,
            value,
            description,
            priority
        )
        self._locators.append(locator)
        return self
    
    def add_class_name(
        self,
        value: str,
        priority: int = 50,
        description: Optional[str] = None
    ) -> 'LocatorBuilder':
        """Add class name locator."""
        locator = Locator(
            LocatorStrategy.CLASS_NAME,
            value,
            description,
            priority
        )
        self._locators.append(locator)
        return self
    
    def add_ios_predicate(
        self,
        value: str,
        priority: int = 30,
        description: Optional[str] = None
    ) -> 'LocatorBuilder':
        """Add iOS predicate locator."""
        locator = Locator(
            LocatorStrategy.IOS_PREDICATE,
            value,
            description,
            priority
        )
        self._locators.append(locator)
        return self
    
    def add_ios_class_chain(
        self,
        value: str,
        priority: int = 40,
        description: Optional[str] = None
    ) -> 'LocatorBuilder':
        """Add iOS class chain locator."""
        locator = Locator(
            LocatorStrategy.IOS_CLASS_CHAIN,
            value,
            description,
            priority
        )
        self._locators.append(locator)
        return self
    
    def add_android_uiautomator(
        self,
        value: str,
        priority: int = 30,
        description: Optional[str] = None
    ) -> 'LocatorBuilder':
        """Add Android UIAutomator locator."""
        locator = Locator(
            LocatorStrategy.ANDROID_UIAUTOMATOR,
            value,
            description,
            priority
        )
        self._locators.append(locator)
        return self
    
    def add_custom(
        self,
        strategy: LocatorStrategy,
        value: str,
        priority: int = 100,
        description: Optional[str] = None
    ) -> 'LocatorBuilder':
        """Add custom locator."""
        locator = Locator(strategy, value, description, priority)
        self._locators.append(locator)
        return self
    
    def build(self) -> list[Locator]:
        """
        Build and return sorted locators.
        
        Returns:
            List of locators sorted by priority
        """
        return sorted(self._locators, key=lambda l: l.priority)
