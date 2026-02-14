"""Pytest configuration and fixtures."""
import pytest
from unittest.mock import Mock, MagicMock
from appium import webdriver
from appium_driver.driver import AppiumDriverWrapper
from appium_driver.session_manager import SessionManager
from appium_driver.capabilities import create_android_capabilities
from config.environment import settings


@pytest.fixture
def mock_driver():
    """Create a mock Appium driver."""
    driver = Mock(spec=webdriver.Remote)
    driver.capabilities = {
        'platformName': 'Android',
        'deviceName': 'Test Device',
        'automationName': 'UiAutomator2'
    }
    driver.page_source = '<hierarchy></hierarchy>'
    driver.contexts = ['NATIVE_APP']
    driver.current_context = 'NATIVE_APP'
    driver.device_time = '2024-01-01 12:00:00'
    driver.battery_info = {'level': 0.8, 'state': 2}
    driver.orientation = 'PORTRAIT'
    
    # Mock methods
    driver.quit = Mock()
    driver.back = Mock()
    driver.close_app = Mock()
    driver.launch_app = Mock()
    driver.reset = Mock()
    driver.install_app = Mock()
    driver.remove_app = Mock()
    driver.activate_app = Mock()
    driver.terminate_app = Mock()
    driver.save_screenshot = Mock(return_value=True)
    driver.swipe = Mock()
    driver.hide_keyboard = Mock()
    driver.is_keyboard_shown = Mock(return_value=False)
    driver.is_locked = Mock(return_value=False)
    driver.lock = Mock()
    driver.unlock = Mock()
    driver.implicitly_wait = Mock()
    driver.switch_to = Mock()
    driver.get_window_size = Mock(return_value={'width': 1080, 'height': 1920})
    
    # Mock find_element
    mock_element = Mock()
    mock_element.text = "Test Text"
    mock_element.is_displayed = Mock(return_value=True)
    mock_element.is_enabled = Mock(return_value=True)
    mock_element.is_selected = Mock(return_value=False)
    mock_element.location = {'x': 100, 'y': 200}
    mock_element.size = {'width': 50, 'height': 30}
    mock_element.click = Mock()
    mock_element.send_keys = Mock()
    mock_element.clear = Mock()
    mock_element.get_attribute = Mock(return_value="test_value")
    
    driver.find_element = Mock(return_value=mock_element)
    driver.find_elements = Mock(return_value=[mock_element])
    
    return driver


@pytest.fixture
def driver_wrapper(mock_driver):
    """Create an AppiumDriverWrapper with mock driver."""
    return AppiumDriverWrapper(mock_driver)


@pytest.fixture
def session_manager():
    """Create a SessionManager instance."""
    return SessionManager(session_timeout_minutes=30)


@pytest.fixture
def mock_session(mock_driver):
    """Create a mock session."""
    from appium_driver.session_manager import Session
    return Session(
        session_id="test-session-123",
        driver=mock_driver,
        capabilities={'platformName': 'Android', 'deviceName': 'Test'}
    )


@pytest.fixture
def android_capabilities():
    """Get Android capabilities."""
    return create_android_capabilities(
        device_name="Test Emulator",
        platform_version="11.0",
        app_package="com.example.app",
        app_activity=".MainActivity"
    )


@pytest.fixture
def sample_locators():
    """Get sample locators for testing."""
    from locators.strategy import LocatorBuilder
    
    builder = LocatorBuilder()
    return builder.add_accessibility_id("test_button", priority=10)\
                  .add_id("com.example:id/button", priority=20)\
                  .add_xpath("//android.widget.Button[@text='Test']", priority=100)\
                  .build()


@pytest.fixture
def nlp_processor():
    """Create NLP processor instance."""
    from ai_engine.nlp_processor import NLPProcessor
    return NLPProcessor()


@pytest.fixture
def test_generator():
    """Create test generator instance."""
    from ai_engine.test_generator import TestGenerator
    return TestGenerator()


@pytest.fixture
async def mcp_client():
    """Create test client for MCP server."""
    from fastapi.testclient import TestClient
    from mcp_server.server import app
    
    client = TestClient(app)
    yield client


# Markers
def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "smoke: mark test as a smoke test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
