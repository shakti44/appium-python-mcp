# Quick Start Guide

## Installation

```bash
# Clone the repository
git clone https://github.com/shakti44/appium-python-mcp.git
cd appium-python-mcp

# Install dependencies
pip install -r requirements.txt

# Configure environment (optional)
cp .env.example .env
# Edit .env with your settings
```

## Starting the Server

```bash
# Start the MCP server
python -m mcp_server.server

# Server will start on http://localhost:8080
# API docs: http://localhost:8080/docs
```

## Quick Examples

### 1. Create a Session

```python
import requests

# Create Android session
response = requests.post("http://localhost:8080/sessions", json={
    "platform": "Android",
    "capabilities": {
        "appPackage": "com.example.app",
        "appActivity": ".MainActivity"
    }
})

session_id = response.json()["session_id"]
print(f"Session created: {session_id}")
```

### 2. Execute Commands

```python
# Click on an element
requests.post("http://localhost:8080/commands", json={
    "session_id": session_id,
    "command": "click on login button"
})

# Type text
requests.post("http://localhost:8080/commands", json={
    "session_id": session_id,
    "command": "type 'user@example.com' in email field"
})

# Swipe gesture
requests.post("http://localhost:8080/commands", json={
    "session_id": session_id,
    "command": "swipe down"
})
```

### 3. Take Screenshot

```python
response = requests.post("http://localhost:8080/screenshots", json={
    "session_id": session_id,
    "name": "my_screenshot"
})

screenshot_path = response.json()["screenshot_path"]
print(f"Screenshot saved: {screenshot_path}")
```

### 4. Generate Test Code

```python
response = requests.post("http://localhost:8080/generate/test", json={
    "test_name": "login_test",
    "commands": [
        "click on login button",
        "type 'user@example.com' in email field",
        "type 'password123' in password field",
        "click on submit button"
    ],
    "description": "Test login flow"
})

test_code = response.json()["test_code"]
print(test_code)

# Save to file
with open("test_login.py", "w") as f:
    f.write(test_code)
```

### 5. Using Python Client Directly

```python
from appium_driver.driver import AppiumDriverWrapper
from appium_driver.session_manager import SessionManager
from ai_engine.command_parser import CommandParser
from ai_engine.nlp_processor import NLPProcessor

# Create session manager
session_manager = SessionManager()
session_id = session_manager.create_session(
    server_url="http://localhost:4723",
    capabilities={
        "platformName": "Android",
        "deviceName": "emulator-5554"
    }
)

# Get driver
driver = session_manager.get_driver(session_id)
driver_wrapper = AppiumDriverWrapper(driver)

# Use NLP to execute commands
nlp = NLPProcessor()
parser = CommandParser(driver_wrapper)

# Parse and execute
command = nlp.parse_command("click on login button")
parser.execute_command(command)
```

### 6. Using Page Objects

```python
from page_objects.example_pages import LoginPage

# Create page object
login_page = LoginPage(driver_wrapper)

# Use page methods
login_page.login("user@example.com", "password123")

# Check for errors
if login_page.is_error_displayed():
    error_msg = login_page.get_error_message()
    print(f"Error: {error_msg}")
```

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_appium_actions.py

# Run with verbose output
pytest -v

# Run unit tests only
pytest -m unit

# Run integration tests only
pytest -m integration
```

## API Endpoints

### Session Management
- `POST /sessions` - Create session
- `GET /sessions` - List all sessions
- `GET /sessions/{session_id}` - Get session info
- `DELETE /sessions/{session_id}` - Delete session

### Command Execution
- `POST /commands` - Execute natural language command
- `POST /elements/action` - Execute element action
- `POST /gestures` - Execute gesture

### Code Generation
- `POST /generate/test` - Generate test code
- `POST /generate/page-object` - Generate page object

### Utilities
- `POST /screenshots` - Take screenshot
- `GET /health` - Health check
- `GET /` - Server info

## Configuration

### Environment Variables

```env
# Server
SERVER_HOST=0.0.0.0
SERVER_PORT=8080

# Appium
APPIUM_SERVER_URL=http://localhost:4723
IMPLICIT_WAIT=10
EXPLICIT_WAIT=30

# Features
SCREENSHOT_ON_FAILURE=true
LOG_LEVEL=INFO
```

### Capabilities

Edit `config/capabilities.json`:

```json
{
  "android": {
    "platformName": "Android",
    "automationName": "UiAutomator2",
    "deviceName": "Android Emulator"
  }
}
```

### Devices

Edit `config/devices.yaml`:

```yaml
devices:
  android_emulators:
    - name: "Pixel_5_API_30"
      udid: "emulator-5554"
      platform: "Android"
      version: "11.0"
```

## Troubleshooting

### Server won't start
- Check if port 8080 is available
- Verify Python 3.11+ is installed
- Ensure all dependencies are installed

### Session creation fails
- Verify Appium server is running on http://localhost:4723
- Check device/emulator is connected
- Review capabilities configuration

### Commands fail
- Check session is active
- Verify element locators
- Review logs for error details

### Tests fail
- Ensure test dependencies are installed
- Check pytest configuration
- Review individual test output

## Support

- Documentation: http://localhost:8080/docs
- Issues: GitHub Issues
- Tests: `pytest tests/ -v`

## Next Steps

1. Start the MCP server
2. Create a session for your device
3. Execute commands via API or Python
4. Generate test code automatically
5. Build page objects for your app
6. Run comprehensive tests

Happy Testing! 🚀
