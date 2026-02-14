"""Tests for Appium actions."""
import pytest
from unittest.mock import Mock, patch
from actions.element_actions import ElementActions
from actions.device_actions import DeviceActions
from actions.gesture_actions import GestureActions


@pytest.mark.unit
class TestElementActions:
    """Test element actions."""
    
    def test_click(self, driver_wrapper, sample_locators):
        """Test click action."""
        actions = ElementActions(driver_wrapper)
        actions.click(sample_locators)
        
        # Verify element was found and clicked
        assert driver_wrapper.driver.find_element.called
    
    def test_send_keys(self, driver_wrapper, sample_locators):
        """Test send keys action."""
        actions = ElementActions(driver_wrapper)
        actions.send_keys(sample_locators, "test input", clear_first=True)
        
        # Verify element was found and keys sent
        assert driver_wrapper.driver.find_element.called
    
    def test_get_text(self, driver_wrapper, sample_locators):
        """Test get text action."""
        actions = ElementActions(driver_wrapper)
        text = actions.get_text(sample_locators)
        
        assert text == "Test Text"
        assert driver_wrapper.driver.find_element.called
    
    def test_is_displayed(self, driver_wrapper, sample_locators):
        """Test is displayed check."""
        actions = ElementActions(driver_wrapper)
        result = actions.is_displayed(sample_locators)
        
        assert result is True
    
    def test_get_attribute(self, driver_wrapper, sample_locators):
        """Test get attribute."""
        actions = ElementActions(driver_wrapper)
        value = actions.get_attribute(sample_locators, "name")
        
        assert value == "test_value"


@pytest.mark.unit
class TestDeviceActions:
    """Test device actions."""
    
    def test_back(self, driver_wrapper):
        """Test back navigation."""
        actions = DeviceActions(driver_wrapper)
        actions.back()
        
        assert driver_wrapper.driver.back.called
    
    def test_lock_unlock(self, driver_wrapper):
        """Test lock and unlock."""
        actions = DeviceActions(driver_wrapper)
        
        actions.lock(5)
        assert driver_wrapper.driver.lock.called
        
        actions.unlock()
        assert driver_wrapper.driver.unlock.called
    
    def test_is_locked(self, driver_wrapper):
        """Test is locked check."""
        actions = DeviceActions(driver_wrapper)
        result = actions.is_locked()
        
        assert result is False
    
    def test_rotate(self, driver_wrapper):
        """Test device rotation."""
        actions = DeviceActions(driver_wrapper)
        actions.rotate("LANDSCAPE")
        
        # Orientation should be set
        assert driver_wrapper.driver.orientation == "LANDSCAPE"
    
    def test_hide_keyboard(self, driver_wrapper):
        """Test hide keyboard."""
        actions = DeviceActions(driver_wrapper)
        actions.hide_keyboard()
        
        assert driver_wrapper.driver.hide_keyboard.called
    
    def test_get_device_time(self, driver_wrapper):
        """Test get device time."""
        actions = DeviceActions(driver_wrapper)
        time = actions.get_device_time()
        
        assert time == "2024-01-01 12:00:00"
    
    def test_get_battery_info(self, driver_wrapper):
        """Test get battery info."""
        actions = DeviceActions(driver_wrapper)
        battery = actions.get_battery_info()
        
        assert battery['level'] == 0.8
        assert battery['state'] == 2


@pytest.mark.unit
class TestGestureActions:
    """Test gesture actions."""
    
    def test_swipe(self, driver_wrapper):
        """Test swipe gesture."""
        actions = GestureActions(driver_wrapper)
        actions.swipe(100, 200, 300, 400, 500)
        
        assert driver_wrapper.driver.swipe.called
    
    def test_swipe_left(self, driver_wrapper):
        """Test swipe left."""
        actions = GestureActions(driver_wrapper)
        actions.swipe_left(500)
        
        assert driver_wrapper.driver.swipe.called
    
    def test_swipe_right(self, driver_wrapper):
        """Test swipe right."""
        actions = GestureActions(driver_wrapper)
        actions.swipe_right(500)
        
        assert driver_wrapper.driver.swipe.called
    
    def test_swipe_up(self, driver_wrapper):
        """Test swipe up."""
        actions = GestureActions(driver_wrapper)
        actions.swipe_up(500)
        
        assert driver_wrapper.driver.swipe.called
    
    def test_swipe_down(self, driver_wrapper):
        """Test swipe down."""
        actions = GestureActions(driver_wrapper)
        actions.swipe_down(500)
        
        assert driver_wrapper.driver.swipe.called
    
    def test_scroll(self, driver_wrapper):
        """Test scroll."""
        actions = GestureActions(driver_wrapper)
        
        actions.scroll(direction="down")
        assert driver_wrapper.driver.swipe.called
        
        actions.scroll(direction="up")
        assert driver_wrapper.driver.swipe.called


@pytest.mark.unit
class TestActionIntegration:
    """Test action integration."""
    
    def test_get_available_actions(self, driver_wrapper):
        """Test getting available actions."""
        element_actions = ElementActions(driver_wrapper)
        device_actions = DeviceActions(driver_wrapper)
        gesture_actions = GestureActions(driver_wrapper)
        
        # Check that actions are available
        assert len(element_actions.get_available_actions()) > 0
        assert len(device_actions.get_available_actions()) > 0
        assert len(gesture_actions.get_available_actions()) > 0
        
        # Verify specific actions exist
        assert 'click' in element_actions.get_available_actions()
        assert 'back' in device_actions.get_available_actions()
        assert 'swipe' in gesture_actions.get_available_actions()
