"""Device-level actions for mobile automation."""
from typing import Optional, Dict, Any
from actions.base_actions import BaseActions
from pathlib import Path


class DeviceActions(BaseActions):
    """Actions for device-level operations."""
    
    def back(self):
        """Navigate back."""
        self.driver.back()
        self.logger.info("Navigated back")
    
    def home(self):
        """Go to home screen (Android)."""
        if self.driver_wrapper.platform_name.lower() == 'android':
            self.driver.press_keycode(3)  # HOME key
            self.logger.info("Pressed home button")
        else:
            self.driver.execute_script('mobile: pressButton', {'name': 'home'})
            self.logger.info("Pressed home button (iOS)")
    
    def lock(self, seconds: Optional[int] = None):
        """
        Lock device.
        
        Args:
            seconds: Optional duration to lock
        """
        if seconds:
            self.driver.lock(seconds)
        else:
            self.driver.lock()
        self.logger.info(f"Device locked{' for ' + str(seconds) + 's' if seconds else ''}")
    
    def unlock(self):
        """Unlock device."""
        self.driver.unlock()
        self.logger.info("Device unlocked")
    
    def is_locked(self) -> bool:
        """
        Check if device is locked.
        
        Returns:
            True if locked, False otherwise
        """
        return self.driver.is_locked()
    
    def rotate(self, orientation: str):
        """
        Rotate device.
        
        Args:
            orientation: PORTRAIT or LANDSCAPE
        """
        self.driver.orientation = orientation
        self.logger.info(f"Device rotated to {orientation}")
    
    def get_orientation(self) -> str:
        """
        Get current orientation.
        
        Returns:
            Current orientation (PORTRAIT or LANDSCAPE)
        """
        return self.driver.orientation
    
    def hide_keyboard(self):
        """Hide keyboard if visible."""
        try:
            self.driver.hide_keyboard()
            self.logger.info("Keyboard hidden")
        except Exception:
            self.logger.debug("No keyboard to hide")
    
    def is_keyboard_shown(self) -> bool:
        """
        Check if keyboard is shown.
        
        Returns:
            True if keyboard visible, False otherwise
        """
        return self.driver.is_keyboard_shown()
    
    def open_notifications(self):
        """Open notifications (Android)."""
        if self.driver_wrapper.platform_name.lower() == 'android':
            self.driver.open_notifications()
            self.logger.info("Opened notifications")
        else:
            self.logger.warning("Notifications not supported on iOS")
    
    def get_device_time(self) -> str:
        """
        Get device time.
        
        Returns:
            Device time as string
        """
        time = self.driver.device_time
        self.logger.info(f"Device time: {time}")
        return time
    
    def get_battery_info(self) -> Dict[str, Any]:
        """
        Get battery information.
        
        Returns:
            Battery info dictionary
        """
        battery = self.driver.battery_info
        self.logger.info(f"Battery info: {battery}")
        return battery
    
    def get_network_connection(self) -> int:
        """
        Get network connection status (Android).
        
        Returns:
            Network connection type
        """
        if self.driver_wrapper.platform_name.lower() == 'android':
            connection = self.driver.network_connection
            self.logger.info(f"Network connection: {connection}")
            return connection
        return 0
    
    def set_network_connection(self, connection_type: int):
        """
        Set network connection (Android).
        
        Args:
            connection_type: 0=None, 1=Airplane, 2=WiFi, 4=Data, 6=All
        """
        if self.driver_wrapper.platform_name.lower() == 'android':
            self.driver.set_network_connection(connection_type)
            self.logger.info(f"Network connection set to: {connection_type}")
        else:
            self.logger.warning("Network connection not supported on iOS")
    
    def toggle_airplane_mode(self):
        """Toggle airplane mode (Android)."""
        if self.driver_wrapper.platform_name.lower() == 'android':
            self.driver.toggle_airplane_mode()
            self.logger.info("Toggled airplane mode")
        else:
            self.logger.warning("Airplane mode toggle not supported on iOS")
    
    def toggle_wifi(self):
        """Toggle WiFi (Android)."""
        if self.driver_wrapper.platform_name.lower() == 'android':
            self.driver.toggle_wifi()
            self.logger.info("Toggled WiFi")
        else:
            self.logger.warning("WiFi toggle not supported on iOS")
    
    def toggle_location_services(self):
        """Toggle location services (Android)."""
        if self.driver_wrapper.platform_name.lower() == 'android':
            self.driver.toggle_location_services()
            self.logger.info("Toggled location services")
        else:
            self.logger.warning("Location services toggle not supported on iOS")
    
    def take_screenshot(self, name: Optional[str] = None) -> Path:
        """
        Take screenshot.
        
        Args:
            name: Optional screenshot name
            
        Returns:
            Path to screenshot file
        """
        return self.driver_wrapper.take_screenshot(name)
    
    def get_page_source(self) -> str:
        """
        Get page source XML.
        
        Returns:
            Page source as string
        """
        source = self.driver.page_source
        self.logger.debug("Retrieved page source")
        return source
    
    def get_contexts(self) -> list:
        """
        Get available contexts.
        
        Returns:
            List of context names
        """
        return self.driver_wrapper.get_contexts()
    
    def get_current_context(self) -> str:
        """
        Get current context.
        
        Returns:
            Current context name
        """
        return self.driver_wrapper.get_current_context()
    
    def switch_to_context(self, context: str):
        """
        Switch to web or native context.
        
        Args:
            context: Context name (NATIVE_APP, WEBVIEW, etc.)
        """
        self.driver_wrapper.switch_to_context(context)
    
    def press_keycode(self, keycode: int):
        """
        Press keycode (Android).
        
        Args:
            keycode: Android keycode
        """
        if self.driver_wrapper.platform_name.lower() == 'android':
            self.driver.press_keycode(keycode)
            self.logger.info(f"Pressed keycode: {keycode}")
        else:
            self.logger.warning("Keycode press not supported on iOS")
    
    def start_recording_screen(self, **options):
        """
        Start screen recording.
        
        Args:
            **options: Recording options
        """
        self.driver.start_recording_screen(**options)
        self.logger.info("Started screen recording")
    
    def stop_recording_screen(self) -> str:
        """
        Stop screen recording.
        
        Returns:
            Base64 encoded video data
        """
        video = self.driver.stop_recording_screen()
        self.logger.info("Stopped screen recording")
        return video
    
    def get_available_actions(self) -> list[str]:
        """Get list of available actions."""
        return [
            'back', 'home', 'lock', 'unlock', 'is_locked',
            'rotate', 'get_orientation', 'hide_keyboard', 'is_keyboard_shown',
            'open_notifications', 'get_device_time', 'get_battery_info',
            'get_network_connection', 'set_network_connection',
            'toggle_airplane_mode', 'toggle_wifi', 'toggle_location_services',
            'take_screenshot', 'get_page_source', 'get_contexts',
            'get_current_context', 'switch_to_context', 'press_keycode',
            'start_recording_screen', 'stop_recording_screen'
        ]
