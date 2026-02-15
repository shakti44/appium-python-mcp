# SETUP.md

## Introduction
This repository contains Python scripts for automated mobile testing using Appium.

## Prerequisites
Before you begin, ensure you have the following installed on your machine:
- **Python 3.x**: A versatile programming language used in this project.
- **pip**: The package installer for Python, which comes pre-installed with Python in most distributions.
- **Appium**: An open-source tool for automating mobile apps.

## Installation Steps

### Step 1: Install Python
If you don't have Python installed, download and install it from the [official Python website](https://www.python.org/downloads/).

### Step 2: Install pip
Pip is generally installed with Python. To check if pip is installed, run:
```bash
pip --version
```
If it's not installed, follow the [installation guide here](https://pip.pypa.io/en/stable/installation/).

### Step 3: Clone the Repository
Open your terminal and run:
```bash
git clone https://github.com/shakti44/appium-python-mcp.git
```

### Step 4: Navigate to the Project Directory
Change your directory to the newly cloned repository:
```bash
cd appium-python-mcp
```

### Step 5: Install Dependencies
Install the required Python packages using pip:
```bash
pip install -r requirements.txt
```

### Step 6: Install Appium
You can install Appium through npm (Node Package Manager). If you don't have Node.js installed, download it from the [Node.js website](https://nodejs.org/). Then run:
```bash
npm install -g appium
```

## Environment Setup
You might need to set up environment variables depending on your operating system. 
- For Windows:
  Set environment variables using the system properties dialog.
- For macOS/Linux:
  You can add the following lines to your `~/.bash_profile` or `~/.bashrc`:
  ```bash
  export PATH=$PATH:/path/to/appium
  ```

## Running the Project
To run the tests, simply execute:
```bash
python -m unittest discover
```

## Troubleshooting
If you encounter any issues, consider checking the following:
- Ensure all dependencies have been installed properly.
- Check Appium server logs for any errors.

## Contributing
We welcome contributions to this project. Please see `CONTRIBUTING.md` for more details.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
