# SETUP.md

## Introduction
This project is a Python-based implementation for Appium, aimed at mobile test automation.

## Prerequisites
1. **Python**: Ensure you have Python 3.x installed. Download it from [python.org](https://www.python.org/downloads/).
2. **Node.js**: Install Node.js which is required to install Appium. Visit [nodejs.org](https://nodejs.org/) for downloading.
3. **Appium**: Install Appium through npm.

## Installation Steps

### Step 1: Installing Python
- Download the Python installer from the official website.
- Run the installer and follow the prompts to install Python. Ensure you check the box to add Python to PATH.

### Step 2: Setting up a Virtual Environment
- Open a terminal or command prompt.
- Navigate to your project directory.
- Create a virtual environment by running:
```bash
python -m venv venv
```
- Activate the virtual environment:
  - **Windows**: `venv\Scripts\activate`
  - **Mac/Linux**: `source venv/bin/activate`

### Step 3: Installing Appium
- Install Appium globally by running:
```bash
npm install -g appium
```

### Step 4: Installing Project Dependencies
- Ensure you are still in your virtual environment.
- Install the necessary Python libraries by running:
```bash
pip install -r requirements.txt
```

### Step 5: Setting up Appium Server
- Start the Appium server by executing:
```bash
appium
```
- Ensure that the server starts without errors.

## Running the Project
- To run the tests, execute the appropriate Python files. For example:
```bash
python test_example.py
```

## Troubleshooting
- **If you encounter issues starting the Appium server**: Ensure all prerequisites are correctly installed.
- **Virtual environment issues**: Ensure it is activated before running Python commands.

## Additional Resources
- [Appium Documentation](http://appium.io/docs/en/about-appium/intro/)
- [Python Documentation](https://docs.python.org/3/)
- [Node.js Documentation](https://nodejs.org/en/docs/)