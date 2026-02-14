# Appium Driver Wrapper

This is an Appium driver wrapper for both Android and iOS platforms. It simplifies the process of initializing the Appium driver and interacting with mobile applications. Below are the key functionalities provided by this wrapper.

## Installation

Make sure to install the required dependencies:  
```bash
pip install Appium-Python-Client
```

## Usage

### Initialize Driver

```python
from appium import webdriver

class AppiumDriver:
    def __init__(self, platform_name, device_name, app, automation_name='UiAutomator2'):
        self.desired_caps = {
            'platformName': platform_name,
            'deviceName': device_name,
            'app': app,
            'automationName': automation_name
        }
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)

    def quit(self):
        self.driver.quit()

    # Additional methods can be added here for interacting with the app
# Usage example:
# driver = AppiumDriver(platform_name='Android', device_name='MyDevice', app='path/to/app.apk')
# driver.quit() 
```

## Additional Methods

You can extend this wrapper with more methods for specific interactions with your mobile application as needed. 
