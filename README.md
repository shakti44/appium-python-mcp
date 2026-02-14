# Appium Python MCP Server

Production-ready, AI-driven MCP-compatible mobile automation server with full Python Appium implementation.

## 🚀 Features

- **FastAPI MCP Server**: High-performance async server with JSON-RPC support
- **Natural Language Commands**: Execute automation using plain English
- **Multi-Platform Support**: Android and iOS with auto-discovery
- **AI-Powered**: Intelligent command parsing and test generation
- **Page Object Model**: Built-in POM framework with smart locators
- **Comprehensive Actions**: Element, device, and gesture operations
- **Session Management**: Multi-session support with lifecycle management
- **Auto Test Generation**: Generate pytest tests from commands
- **Smart Locators**: Multi-strategy fallback for robust element finding
- **Rich Reporting**: HTML/JSON reports with screenshots

## 📋 Prerequisites

- Python 3.11+
- Appium Server 2.0+ ([Installation Guide](http://appium.io))
- Android SDK (for Android testing)
- Xcode (for iOS testing on macOS)

## 🔧 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/shakti44/appium-python-mcp.git
   cd appium-python-mcp
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment** (optional):
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file:

```env
SERVER_HOST=0.0.0.0
SERVER_PORT=8080
APPIUM_SERVER_URL=http://localhost:4723
LOG_LEVEL=INFO
SCREENSHOT_ON_FAILURE=true
```

### Capabilities Configuration

Edit `config/capabilities.json` for platform-specific settings:

```json
{
  "android": {
    "platformName": "Android",
    "automationName": "UiAutomator2",
    "deviceName": "Android Emulator"
  },
  "ios": {
    "platformName": "iOS",
    "automationName": "XCUITest",
    "deviceName": "iPhone 14"
  }
}
```

## 🚀 Usage

### Start the MCP Server

```bash
python -m mcp_server.server
```

Or programmatically:

```python
from mcp_server.server import start_server
start_server(host="0.0.0.0", port=8080)
```

### API Documentation

Once running, access interactive API docs at:
- Swagger UI: `http://localhost:8080/docs`
- ReDoc: `http://localhost:8080/redoc`

## 📘 Examples

### 1. Create a Session

```python
import requests

response = requests.post("http://localhost:8080/sessions", json={
    "platform": "Android",
    "capabilities": {
        "appPackage": "com.example.app",
        "appActivity": ".MainActivity"
    }
})

session_id = response.json()["session_id"]
```

### 2. Execute Natural Language Commands

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

### 3. Generate Test Code

```python
response = requests.post("http://localhost:8080/generate/test", json={
    "test_name": "login_test",
    "commands": [
        "click on login button",
        "type 'test@example.com' in email field",
        "click on submit button"
    ],
    "description": "Test login flow"
})

print(response.json()["test_code"])
```

### 4. Using Page Objects

```python
from appium_driver.driver import AppiumDriverWrapper
from page_objects.example_pages import LoginPage

# Create driver wrapper (after session creation)
driver_wrapper = AppiumDriverWrapper(driver)

# Use page object
login_page = LoginPage(driver_wrapper)
login_page.login("user@example.com", "password123")
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test types
pytest -m unit
pytest -m integration
pytest -m smoke
```

## 📊 Architecture

```
appium-python-mcp/
├── mcp_server/          # FastAPI MCP server
├── appium_driver/       # Driver wrapper & session management
├── actions/             # Element, device & gesture actions
├── ai_engine/           # NLP processor & test generator
├── locators/            # Smart locator strategies
├── page_objects/        # Page Object Model base
├── config/              # Configuration files
├── utils/               # Logging, reporting & helpers
└── tests/               # Comprehensive test suite
```

## 🤖 AI Features

### Natural Language Processing

The NLP engine understands commands like:
- "click on the login button"
- "type 'username' in the email field"
- "swipe left 3 times"
- "verify that welcome message is displayed"

### Auto Test Generation

Generate pytest tests from plain English:

```python
from ai_engine.test_generator import TestGenerator
from ai_engine.nlp_processor import NLPProcessor

nlp = NLPProcessor()
generator = TestGenerator()

commands = [
    nlp.parse_command("click on login"),
    nlp.parse_command("type 'user' in username"),
]

test_code = generator.generate_test_from_commands(
    test_name="login_test",
    commands=commands
)
```

## 📈 Reporting

Tests automatically generate:
- HTML reports with screenshots
- JSON reports for CI integration
- Execution metrics and timing

Access reports in the `reports/` directory.

## 🔐 Security

- No hardcoded credentials
- Environment-based configuration
- Session timeout protection
- Input validation on all endpoints

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Appium Python Client](https://github.com/appium/python-client)
- Powered by [FastAPI](https://fastapi.tiangolo.com/)
- Inspired by the Model Context Protocol

## 📞 Support

- 📫 Issues: [GitHub Issues](https://github.com/shakti44/appium-python-mcp/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/shakti44/appium-python-mcp/discussions)

---

Made with ❤️ by the Appium Python MCP team