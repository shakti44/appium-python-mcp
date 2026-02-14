"""Gesture actions for mobile automation."""
from typing import Optional, Tuple
from actions.base_actions import BaseActions
from locators.strategy import Locator
from locators.locator_engine import LocatorEngine


class GestureActions(BaseActions):
    """Actions for gestures and touch interactions."""
    
    def __init__(self, driver_wrapper):
        """Initialize gesture actions."""
        super().__init__(driver_wrapper)
        self.locator_engine = LocatorEngine(driver_wrapper)
    
    def swipe(
        self,
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
        duration: int = 500
    ):
        """
        Perform swipe gesture.
        
        Args:
            start_x: Starting X coordinate
            start_y: Starting Y coordinate
            end_x: Ending X coordinate
            end_y: Ending Y coordinate
            duration: Swipe duration in milliseconds
        """
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)
        self.logger.info(f"Swiped from ({start_x}, {start_y}) to ({end_x}, {end_y})")
    
    def swipe_left(self, duration: int = 500):
        """
        Swipe left across screen.
        
        Args:
            duration: Swipe duration in milliseconds
        """
        size = self.driver.get_window_size()
        start_x = int(size['width'] * 0.8)
        end_x = int(size['width'] * 0.2)
        y = int(size['height'] * 0.5)
        
        self.swipe(start_x, y, end_x, y, duration)
        self.logger.info("Swiped left")
    
    def swipe_right(self, duration: int = 500):
        """
        Swipe right across screen.
        
        Args:
            duration: Swipe duration in milliseconds
        """
        size = self.driver.get_window_size()
        start_x = int(size['width'] * 0.2)
        end_x = int(size['width'] * 0.8)
        y = int(size['height'] * 0.5)
        
        self.swipe(start_x, y, end_x, y, duration)
        self.logger.info("Swiped right")
    
    def swipe_up(self, duration: int = 500):
        """
        Swipe up across screen.
        
        Args:
            duration: Swipe duration in milliseconds
        """
        size = self.driver.get_window_size()
        x = int(size['width'] * 0.5)
        start_y = int(size['height'] * 0.8)
        end_y = int(size['height'] * 0.2)
        
        self.swipe(x, start_y, x, end_y, duration)
        self.logger.info("Swiped up")
    
    def swipe_down(self, duration: int = 500):
        """
        Swipe down across screen.
        
        Args:
            duration: Swipe duration in milliseconds
        """
        size = self.driver.get_window_size()
        x = int(size['width'] * 0.5)
        start_y = int(size['height'] * 0.2)
        end_y = int(size['height'] * 0.8)
        
        self.swipe(x, start_y, x, end_y, duration)
        self.logger.info("Swiped down")
    
    def scroll(
        self,
        direction: str = "down",
        distance: float = 0.5,
        duration: int = 500
    ):
        """
        Scroll in a direction.
        
        Args:
            direction: Scroll direction (up, down, left, right)
            distance: Scroll distance as percentage (0.0 to 1.0)
            duration: Scroll duration in milliseconds
        """
        if direction == "down":
            self.swipe_up(duration)
        elif direction == "up":
            self.swipe_down(duration)
        elif direction == "left":
            self.swipe_right(duration)
        elif direction == "right":
            self.swipe_left(duration)
        else:
            raise ValueError(f"Invalid direction: {direction}")
    
    def tap(self, x: int, y: int, count: int = 1):
        """
        Tap at coordinates.
        
        Args:
            x: X coordinate
            y: Y coordinate
            count: Number of taps
        """
        from appium.webdriver.common.touch_action import TouchAction
        
        action = TouchAction(self.driver)
        for _ in range(count):
            action.tap(x=x, y=y).perform()
        
        self.logger.info(f"Tapped at ({x}, {y}) {count} time(s)")
    
    def tap_element(
        self,
        locators: list[Locator],
        count: int = 1,
        timeout: Optional[int] = None
    ):
        """
        Tap an element.
        
        Args:
            locators: List of locators to try
            count: Number of taps
            timeout: Optional custom timeout
        """
        from appium.webdriver.common.touch_action import TouchAction
        
        element = self.locator_engine.find_element_with_fallback(locators, timeout)
        action = TouchAction(self.driver)
        
        for _ in range(count):
            action.tap(element).perform()
        
        self.logger.info(f"Tapped element {count} time(s)")
    
    def double_tap(self, x: int, y: int):
        """
        Double tap at coordinates.
        
        Args:
            x: X coordinate
            y: Y coordinate
        """
        self.tap(x, y, count=2)
        self.logger.info(f"Double tapped at ({x}, {y})")
    
    def long_press(
        self,
        x: int,
        y: int,
        duration: int = 1000
    ):
        """
        Long press at coordinates.
        
        Args:
            x: X coordinate
            y: Y coordinate
            duration: Press duration in milliseconds
        """
        from appium.webdriver.common.touch_action import TouchAction
        
        action = TouchAction(self.driver)
        action.long_press(x=x, y=y, duration=duration).release().perform()
        
        self.logger.info(f"Long pressed at ({x}, {y}) for {duration}ms")
    
    def drag_and_drop(
        self,
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
        duration: int = 1000
    ):
        """
        Drag and drop gesture.
        
        Args:
            start_x: Starting X coordinate
            start_y: Starting Y coordinate
            end_x: Ending X coordinate
            end_y: Ending Y coordinate
            duration: Drag duration in milliseconds
        """
        from appium.webdriver.common.touch_action import TouchAction
        
        action = TouchAction(self.driver)
        action.long_press(x=start_x, y=start_y, duration=duration)
        action.move_to(x=end_x, y=end_y)
        action.release().perform()
        
        self.logger.info(f"Dragged from ({start_x}, {start_y}) to ({end_x}, {end_y})")
    
    def pinch(self, scale: float = 0.5):
        """
        Pinch gesture (zoom out).
        
        Args:
            scale: Scale factor (0.0 to 1.0)
        """
        if self.driver_wrapper.platform_name.lower() == 'ios':
            self.driver.execute_script('mobile: pinch', {'scale': scale})
            self.logger.info(f"Pinched with scale {scale}")
        else:
            # Android pinch using MultiAction
            size = self.driver.get_window_size()
            center_x = size['width'] // 2
            center_y = size['height'] // 2
            offset = int(size['width'] * 0.2 * scale)
            
            from appium.webdriver.common.multi_action import MultiAction
            from appium.webdriver.common.touch_action import TouchAction
            
            action1 = TouchAction(self.driver)
            action1.press(x=center_x - offset, y=center_y).move_to(x=center_x, y=center_y).release()
            
            action2 = TouchAction(self.driver)
            action2.press(x=center_x + offset, y=center_y).move_to(x=center_x, y=center_y).release()
            
            multi_action = MultiAction(self.driver)
            multi_action.add(action1, action2)
            multi_action.perform()
            
            self.logger.info("Pinched (Android)")
    
    def zoom(self, scale: float = 2.0):
        """
        Zoom gesture (zoom in).
        
        Args:
            scale: Scale factor (> 1.0)
        """
        if self.driver_wrapper.platform_name.lower() == 'ios':
            self.driver.execute_script('mobile: pinch', {'scale': scale})
            self.logger.info(f"Zoomed with scale {scale}")
        else:
            # Android zoom using MultiAction
            size = self.driver.get_window_size()
            center_x = size['width'] // 2
            center_y = size['height'] // 2
            offset = int(size['width'] * 0.2)
            
            from appium.webdriver.common.multi_action import MultiAction
            from appium.webdriver.common.touch_action import TouchAction
            
            action1 = TouchAction(self.driver)
            action1.press(x=center_x, y=center_y).move_to(x=center_x - offset, y=center_y).release()
            
            action2 = TouchAction(self.driver)
            action2.press(x=center_x, y=center_y).move_to(x=center_x + offset, y=center_y).release()
            
            multi_action = MultiAction(self.driver)
            multi_action.add(action1, action2)
            multi_action.perform()
            
            self.logger.info("Zoomed (Android)")
    
    def flick(
        self,
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int
    ):
        """
        Fast flick gesture.
        
        Args:
            start_x: Starting X coordinate
            start_y: Starting Y coordinate
            end_x: Ending X coordinate
            end_y: Ending Y coordinate
        """
        self.swipe(start_x, start_y, end_x, end_y, duration=200)
        self.logger.info(f"Flicked from ({start_x}, {start_y}) to ({end_x}, {end_y})")
    
    def get_available_actions(self) -> list[str]:
        """Get list of available actions."""
        return [
            'swipe', 'swipe_left', 'swipe_right', 'swipe_up', 'swipe_down',
            'scroll', 'tap', 'tap_element', 'double_tap', 'long_press',
            'drag_and_drop', 'pinch', 'zoom', 'flick'
        ]
