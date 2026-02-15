# Appium Python MCP Server

A comprehensive MCP (Model Context Protocol) server for Appium mobile automation, built with FastAPI.

## Features

- **Session Management**: Create, manage, and track Appium sessions
- **Device Handling**: List and interact with connected Android/iOS devices
- **Command Processing**: Execute Appium commands through a RESTful API
- **Async Support**: Built on FastAPI for high-performance async operations

## Installation

Install dependencies using pip:

```bash
pip install -r requirements.txt
```

Or using Poetry:

```bash
poetry install
```

## Quick Start

### Running the Server

```bash
python main.py
```

The server will start on `http://0.0.0.0:8000` by default.

For custom host/port:

```bash
python main.py --host localhost --port 5000
```

For development with auto-reload:

```bash
python main.py --reload
```

### API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Health Check
- `GET /` - Root endpoint
- `GET /health` - Health check

### Session Management
- `POST /session/` - Create a new Appium session
- `GET /session/{session_id}` - Get session details
- `DELETE /session/{session_id}` - Delete a session
- `GET /sessions/` - List all active sessions

### Command Processing
- `POST /command/` - Execute an Appium command

### Device Management
- `GET /devices/` - List all connected devices
- `GET /device/{device_id}` - Get device status
- `POST /device/command/` - Send command to device

### Server Management
- `POST /server/cleanup` - Cleanup expired sessions

## Usage Examples

### Create a Session

```bash
curl -X POST "http://localhost:8000/session/" \
  -H "Content-Type: application/json" \
  -d '{
    "platform_name": "Android",
    "device_name": "emulator-5554",
    "app": "/path/to/app.apk",
    "automation_name": "UiAutomator2"
  }'
```

### List Devices

```bash
curl -X GET "http://localhost:8000/devices/"
```

### Execute Command

```bash
curl -X POST "http://localhost:8000/command/" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "your-session-id",
    "command": "tap",
    "parameters": {"x": 100, "y": 200}
  }'
```

## Development

### Running Tests

```bash
pytest tests/ -v
```

### Project Structure

```
appium-python-mcp/
├── appium_driver/         # Appium driver wrapper
│   ├── __init__.py
│   └── driver.py
├── mcp_server/           # FastAPI server
│   ├── __init__.py
│   └── server.py
├── src/                  # Core functionality
│   ├── __init__.py
│   ├── session_manager.py
│   └── device_handler.py
├── tests/                # Test suite
│   ├── __init__.py
│   └── test_session_manager.py
├── main.py              # Entry point
├── requirements.txt     # Dependencies
└── pyproject.toml      # Project configuration
```

## Requirements

- Python 3.8+
- Appium Server (for mobile automation)
- ADB (for Android devices)

## License

MIT