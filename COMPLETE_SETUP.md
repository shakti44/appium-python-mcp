# COMPLETE_SETUP.md

## Setting Up the Python Appium MCP Server

This guide will walk you through the setup process for using the Python Appium MCP Server in both Visual Studio Code and PyCharm. You'll also learn how to configure it with Claude/Cursor.

### Prerequisites
Before you begin, ensure you have the following installed:
- Python 3.6 or higher
- Node.js (latest version recommended)
- Appium

### Installation Steps

#### Step 1: Install Python and Node.js
1. Download Python from the [official website](https://www.python.org/downloads/).
2. Download Node.js from the [official website](https://nodejs.org/).

#### Step 2: Install Appium
1. Open your terminal.
2. Run the following command to install Appium globally:
   ```bash
   npm install -g appium
   ```

#### Step 3: Install Required Python Packages
1. Create a new directory for your project:
   ```bash
   mkdir appium-python-mcp
   cd appium-python-mcp
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install the required packages:
   ```bash
   pip install Appium-Python-Client
   ```

### Setting Up in Visual Studio Code
1. Open Visual Studio Code.
2. Open the project folder (`appium-python-mcp`).
3. Open a terminal in VS Code (`` Ctrl + ` ``).
4. Ensure your virtual environment is activated.
5. Create a new Python file (e.g., `test_appium.py`) and add your test code.

### Setting Up in PyCharm
1. Open PyCharm and create a new project.
2. Select the option to use an existing interpreter and point it to the Python executable in your virtual environment.
3. Create a new Python file (e.g., `test_appium.py`) and add your test code.

### Configuring with Claude/Cursor
1. Install Claude/Cursor plugin according to their documentation.
2. Ensure that it’s pointed to the right Python interpreter (the one in your virtual environment).
3. Use the plugin's features to assist in writing and managing your Appium tests.

### Running Your Tests
1. To run your tests, simply execute the Python script using the following command in the terminal:
   ```bash
   python test_appium.py
   ```

### Conclusion
Now you have a fully functional setup of the Python Appium MCP Server with both VS Code and PyCharm. Happy testing!