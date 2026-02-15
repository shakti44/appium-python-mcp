# Complete Setup Guide for Appium with Python

## Introduction
This guide provides step-by-step instructions for setting up Appium with Python for mobile automation testing. It is aimed at beginners who want to get started with mobile testing using Python.

## Prerequisites
Before you begin, ensure that you have the following installed:

- **Python 3.x**: Download and install Python from [python.org](https://www.python.org/).
- **Node.js**: Download and install Node.js from [nodejs.org](https://nodejs.org/).
- **Appium**: Install Appium using npm (Node Package Manager).

## Step 1: Install Appium
1. Open a terminal or command prompt.
2. Run the following command to install Appium globally:
    ```bash
    npm install -g appium
    ```
3. Verify the installation by running:
    ```bash
    appium -v
    ```

## Step 2: Install Appium Doctor
Appium Doctor is a command-line tool that helps ensure that all of the dependencies are correctly set up.
1. Install Appium Doctor:
    ```bash
    npm install -g appium-doctor
    ```
2. Check your setup:
    ```bash
    appium-doctor
    ```
   Follow the recommendations provided by Appium Doctor to resolve any issues.

## Step 3: Install Python Packages
1. Open a terminal or command prompt.
2. Install the required Python packages by running:
    ```bash
    pip install Appium-Python-Client
    ```

## Step 4: Set Up Android SDK
1. Download and install Android Studio from [developer.android.com](https://developer.android.com/studio).
2. Open Android Studio and follow the setup wizard to install the SDK components. Make a note of the SDK path.
3. Set up environment variables:
   - **ANDROID_HOME**: Path to your Android SDK.
   - **Path**: Add the following to your system's PATH variable:
     - `ANDROID_HOME/tools`
     - `ANDROID_HOME/platform-tools`

## Step 5: Enable Developer Options and USB Debugging on Android Device
1. Go to **Settings** on your Android device.
2. Tap on **About phone** and find **Build number**. Tap it 7 times to enable Developer Options.
3. Go back to **Settings**, tap **Developer options**, and enable **USB Debugging**.

## Step 6: Connect Your Device
1. Connect your Android device to your computer via USB.
2. Grant permission for USB debugging if prompted on your device.

## Step 7: Create a Simple Appium Test
1. Create a new Python file (e.g., `test_appium.py`).
2. Write a simple test script:
    ```python
    from appium import webdriver
    
    desired_caps = {
        'platformName': 'Android',
        'deviceName': 'MyDevice',  # Change this to your device name
        'app': 'path/to/your/app.apk'  # Change this to your app path
    }
    
    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    
    # Your test script goes here
    
    driver.quit()
    ```
3. Save the file.

## Step 8: Start Appium Server
1. Open a terminal or command prompt.
2. Start the Appium server by executing:
    ```bash
    appium
    ```

## Step 9: Run Your Test
1. In another terminal or command prompt, navigate to the directory where your test script is located.
2. Run the test:
    ```bash
    python test_appium.py
    ```

## Conclusion
You have successfully set up Appium with Python! You can now start writing and running your automated tests for mobile applications. 

For more advanced usage, visit the [Appium documentation](http://appium.io/docs/en/about-appium/intro/).