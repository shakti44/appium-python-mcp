"""Command parser to map parsed commands to Appium actions."""
from typing import Dict, Any, Optional, Callable
from ai_engine.nlp_processor import ParsedCommand
from actions.element_actions import ElementActions
from actions.device_actions import DeviceActions
from actions.gesture_actions import GestureActions
from locators.locator_engine import LocatorEngine
from appium_driver.driver import AppiumDriverWrapper
from utils.logger import logger


class CommandParser:
    """Parser to convert parsed commands to executable actions."""
    
    def __init__(self, driver_wrapper: AppiumDriverWrapper):
        """
        Initialize command parser.
        
        Args:
            driver_wrapper: Appium driver wrapper instance
        """
        self.driver_wrapper = driver_wrapper
        self.element_actions = ElementActions(driver_wrapper)
        self.device_actions = DeviceActions(driver_wrapper)
        self.gesture_actions = GestureActions(driver_wrapper)
        self.locator_engine = LocatorEngine(driver_wrapper)
        self.logger = logger
        
        # Map actions to handlers
        self.action_handlers: Dict[str, Callable] = {
            'click': self._handle_click,
            'type': self._handle_type,
            'swipe': self._handle_swipe,
            'wait': self._handle_wait,
            'verify': self._handle_verify,
            'open': self._handle_open,
            'close': self._handle_close,
            'navigate': self._handle_navigate,
            'back': self._handle_back,
            'screenshot': self._handle_screenshot,
            'get': self._handle_get,
            'find': self._handle_find,
        }
    
    def execute_command(self, command: ParsedCommand) -> Any:
        """
        Execute a parsed command.
        
        Args:
            command: ParsedCommand object
            
        Returns:
            Command execution result
        """
        self.logger.info(f"Executing command: {command.action} on {command.target}")
        
        handler = self.action_handlers.get(command.action)
        if not handler:
            raise ValueError(f"No handler for action: {command.action}")
        
        try:
            result = handler(command)
            self.logger.info(f"Command executed successfully: {command.action}")
            return result
        except Exception as e:
            self.logger.error(f"Command execution failed: {e}")
            self.driver_wrapper.take_screenshot(f"error_{command.action}")
            raise
    
    def _create_locators_from_target(self, target: str):
        """Create locators from target text."""
        platform = self.driver_wrapper.platform_name
        
        # Try to create smart locators
        return self.locator_engine.create_smart_locator(
            text=target,
            accessibility_id=target,
            resource_id=target,
            platform=platform
        )
    
    def _handle_click(self, command: ParsedCommand) -> None:
        """Handle click action."""
        if not command.target:
            raise ValueError("Click action requires a target")
        
        locators = self._create_locators_from_target(command.target)
        
        count = command.params.get('count', 1)
        if count > 1:
            # Multiple taps
            self.gesture_actions.tap_element(locators, count=count)
        else:
            # Single click
            self.element_actions.click(locators)
    
    def _handle_type(self, command: ParsedCommand) -> None:
        """Handle type action."""
        if not command.target:
            raise ValueError("Type action requires a target")
        if not command.value:
            raise ValueError("Type action requires a value")
        
        locators = self._create_locators_from_target(command.target)
        self.element_actions.send_keys(locators, command.value)
    
    def _handle_swipe(self, command: ParsedCommand) -> None:
        """Handle swipe action."""
        direction = command.params.get('direction', 'up')
        duration = command.params.get('duration', 500)
        
        if direction == 'up':
            self.gesture_actions.swipe_up(duration)
        elif direction == 'down':
            self.gesture_actions.swipe_down(duration)
        elif direction == 'left':
            self.gesture_actions.swipe_left(duration)
        elif direction == 'right':
            self.gesture_actions.swipe_right(duration)
        else:
            raise ValueError(f"Invalid swipe direction: {direction}")
    
    def _handle_wait(self, command: ParsedCommand) -> None:
        """Handle wait action."""
        import time
        
        duration = command.params.get('duration', 1000)
        seconds = duration / 1000.0
        
        if command.target:
            # Wait for element
            locators = self._create_locators_from_target(command.target)
            self.element_actions.wait_for_element(locators, timeout=int(seconds))
        else:
            # Just wait
            time.sleep(seconds)
    
    def _handle_verify(self, command: ParsedCommand) -> bool:
        """Handle verify action."""
        if not command.target:
            raise ValueError("Verify action requires a target")
        
        locators = self._create_locators_from_target(command.target)
        
        if command.value:
            # Verify text matches
            actual_text = self.element_actions.get_text(locators)
            expected_text = command.value
            
            if expected_text.lower() in actual_text.lower():
                self.logger.info(f"Verification passed: '{actual_text}' contains '{expected_text}'")
                return True
            else:
                self.logger.error(f"Verification failed: '{actual_text}' does not contain '{expected_text}'")
                return False
        else:
            # Just verify element exists
            return self.element_actions.is_displayed(locators)
    
    def _handle_open(self, command: ParsedCommand) -> None:
        """Handle open action."""
        if command.target:
            # Open specific app
            self.driver_wrapper.activate_app(command.target)
        else:
            # Launch current app
            self.device_actions.launch_app()
    
    def _handle_close(self, command: ParsedCommand) -> None:
        """Handle close action."""
        if command.target:
            # Close specific app
            self.driver_wrapper.terminate_app(command.target)
        else:
            # Close current app
            self.device_actions.close_app()
    
    def _handle_navigate(self, command: ParsedCommand) -> None:
        """Handle navigate action."""
        if not command.target:
            raise ValueError("Navigate action requires a target")
        
        # Try to click on navigation target
        locators = self._create_locators_from_target(command.target)
        self.element_actions.click(locators)
    
    def _handle_back(self, command: ParsedCommand) -> None:
        """Handle back action."""
        self.device_actions.back()
    
    def _handle_screenshot(self, command: ParsedCommand) -> str:
        """Handle screenshot action."""
        name = command.target or "manual_screenshot"
        path = self.device_actions.take_screenshot(name)
        return str(path)
    
    def _handle_get(self, command: ParsedCommand) -> str:
        """Handle get action."""
        if not command.target:
            raise ValueError("Get action requires a target")
        
        locators = self._create_locators_from_target(command.target)
        
        # Get text by default
        return self.element_actions.get_text(locators)
    
    def _handle_find(self, command: ParsedCommand) -> bool:
        """Handle find action."""
        if not command.target:
            raise ValueError("Find action requires a target")
        
        locators = self._create_locators_from_target(command.target)
        return self.locator_engine.is_element_present(locators)
    
    def execute_command_sequence(self, commands: list[ParsedCommand]) -> list[Any]:
        """
        Execute a sequence of commands.
        
        Args:
            commands: List of ParsedCommand objects
            
        Returns:
            List of results
        """
        results = []
        
        for i, command in enumerate(commands):
            self.logger.info(f"Executing step {i + 1}/{len(commands)}: {command.action}")
            
            try:
                result = self.execute_command(command)
                results.append(result)
            except Exception as e:
                self.logger.error(f"Step {i + 1} failed: {e}")
                results.append(None)
                # Continue with remaining steps
        
        return results
    
    def get_available_actions(self) -> list[str]:
        """Get list of available actions."""
        return list(self.action_handlers.keys())
