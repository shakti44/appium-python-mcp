"""Base actions interface for mobile automation."""
from abc import ABC, abstractmethod
from typing import Any, Optional
from appium_driver.driver import AppiumDriverWrapper
from utils.logger import logger


class BaseActions(ABC):
    """Abstract base class for all action types."""
    
    def __init__(self, driver_wrapper: AppiumDriverWrapper):
        """
        Initialize base actions.
        
        Args:
            driver_wrapper: Appium driver wrapper instance
        """
        self.driver_wrapper = driver_wrapper
        self.driver = driver_wrapper.driver
        self.logger = logger
    
    def execute_action(self, action_name: str, **kwargs) -> Any:
        """
        Execute an action with error handling and logging.
        
        Args:
            action_name: Name of the action to execute
            **kwargs: Action parameters
            
        Returns:
            Action result
        """
        try:
            self.logger.info(f"Executing action: {action_name} with params: {kwargs}")
            
            # Get the method by name
            if hasattr(self, action_name):
                method = getattr(self, action_name)
                result = method(**kwargs)
                
                self.logger.info(f"Action {action_name} completed successfully")
                return result
            else:
                raise AttributeError(f"Action '{action_name}' not found")
                
        except Exception as e:
            self.logger.error(f"Action {action_name} failed: {e}")
            self.driver_wrapper.take_screenshot(f"error_{action_name}")
            raise
    
    @abstractmethod
    def get_available_actions(self) -> list[str]:
        """
        Get list of available action names.
        
        Returns:
            List of action method names
        """
        pass
