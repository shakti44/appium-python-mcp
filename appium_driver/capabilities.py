"""Appium capabilities management."""
from typing import Dict, Any, Optional
from enum import Enum


class Platform(str, Enum):
    """Supported platforms."""
    ANDROID = "Android"
    IOS = "iOS"


class AutomationName(str, Enum):
    """Automation framework names."""
    UIAUTOMATOR2 = "UiAutomator2"
    XCUITEST = "XCUITest"
    ESPRESSO = "Espresso"


class CapabilitiesBuilder:
    """Builder for Appium capabilities."""
    
    def __init__(self):
        """Initialize capabilities builder."""
        self._capabilities: Dict[str, Any] = {}
    
    def set_platform(self, platform: Platform) -> 'CapabilitiesBuilder':
        """Set platform name."""
        self._capabilities['platformName'] = platform.value
        return self
    
    def set_automation_name(self, automation: AutomationName) -> 'CapabilitiesBuilder':
        """Set automation framework."""
        self._capabilities['automationName'] = automation.value
        return self
    
    def set_device_name(self, name: str) -> 'CapabilitiesBuilder':
        """Set device name."""
        self._capabilities['deviceName'] = name
        return self
    
    def set_platform_version(self, version: str) -> 'CapabilitiesBuilder':
        """Set platform version."""
        self._capabilities['platformVersion'] = version
        return self
    
    def set_app(self, app_path: str) -> 'CapabilitiesBuilder':
        """Set application path."""
        self._capabilities['app'] = app_path
        return self
    
    def set_app_package(self, package: str) -> 'CapabilitiesBuilder':
        """Set Android app package."""
        self._capabilities['appPackage'] = package
        return self
    
    def set_app_activity(self, activity: str) -> 'CapabilitiesBuilder':
        """Set Android app activity."""
        self._capabilities['appActivity'] = activity
        return self
    
    def set_bundle_id(self, bundle_id: str) -> 'CapabilitiesBuilder':
        """Set iOS bundle ID."""
        self._capabilities['bundleId'] = bundle_id
        return self
    
    def set_udid(self, udid: str) -> 'CapabilitiesBuilder':
        """Set device UDID."""
        self._capabilities['udid'] = udid
        return self
    
    def set_no_reset(self, no_reset: bool = True) -> 'CapabilitiesBuilder':
        """Set no reset flag."""
        self._capabilities['noReset'] = no_reset
        return self
    
    def set_full_reset(self, full_reset: bool = False) -> 'CapabilitiesBuilder':
        """Set full reset flag."""
        self._capabilities['fullReset'] = full_reset
        return self
    
    def set_auto_grant_permissions(self, grant: bool = True) -> 'CapabilitiesBuilder':
        """Set auto grant permissions (Android)."""
        self._capabilities['autoGrantPermissions'] = grant
        return self
    
    def set_new_command_timeout(self, timeout: int = 300) -> 'CapabilitiesBuilder':
        """Set new command timeout in seconds."""
        self._capabilities['newCommandTimeout'] = timeout
        return self
    
    def set_custom_capability(self, key: str, value: Any) -> 'CapabilitiesBuilder':
        """Set custom capability."""
        self._capabilities[key] = value
        return self
    
    def build(self) -> Dict[str, Any]:
        """Build and return capabilities dictionary."""
        return self._capabilities.copy()


def create_android_capabilities(
    device_name: str = "Android Emulator",
    platform_version: str = "11.0",
    app_path: Optional[str] = None,
    app_package: Optional[str] = None,
    app_activity: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Create Android capabilities.
    
    Args:
        device_name: Device name
        platform_version: Android version
        app_path: Path to APK file
        app_package: App package name
        app_activity: Main activity name
        **kwargs: Additional capabilities
        
    Returns:
        Capabilities dictionary
    """
    builder = CapabilitiesBuilder()
    builder.set_platform(Platform.ANDROID)
    builder.set_automation_name(AutomationName.UIAUTOMATOR2)
    builder.set_device_name(device_name)
    builder.set_platform_version(platform_version)
    builder.set_auto_grant_permissions(True)
    builder.set_new_command_timeout(300)
    
    if app_path:
        builder.set_app(app_path)
    
    if app_package:
        builder.set_app_package(app_package)
    
    if app_activity:
        builder.set_app_activity(app_activity)
    
    for key, value in kwargs.items():
        builder.set_custom_capability(key, value)
    
    return builder.build()


def create_ios_capabilities(
    device_name: str = "iPhone 14",
    platform_version: str = "16.0",
    app_path: Optional[str] = None,
    bundle_id: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Create iOS capabilities.
    
    Args:
        device_name: Device name
        platform_version: iOS version
        app_path: Path to .app or .ipa file
        bundle_id: Bundle identifier
        **kwargs: Additional capabilities
        
    Returns:
        Capabilities dictionary
    """
    builder = CapabilitiesBuilder()
    builder.set_platform(Platform.IOS)
    builder.set_automation_name(AutomationName.XCUITEST)
    builder.set_device_name(device_name)
    builder.set_platform_version(platform_version)
    builder.set_new_command_timeout(300)
    
    if app_path:
        builder.set_app(app_path)
    
    if bundle_id:
        builder.set_bundle_id(bundle_id)
    
    for key, value in kwargs.items():
        builder.set_custom_capability(key, value)
    
    return builder.build()
