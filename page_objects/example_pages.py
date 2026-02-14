"""Example page objects demonstrating usage."""
from page_objects.base_page import BasePage
from locators.strategy import LocatorStrategy


class LoginPage(BasePage):
    """Example login page object."""
    
    def __init__(self, driver_wrapper):
        """Initialize login page."""
        super().__init__(driver_wrapper)
        
        # Define locators
        self.username_locators = self.locator_engine.create_smart_locator(
            accessibility_id="username_field",
            resource_id="com.example.app:id/username",
            xpath="//android.widget.EditText[@resource-id='username']",
            platform=self.platform
        )
        
        self.password_locators = self.locator_engine.create_smart_locator(
            accessibility_id="password_field",
            resource_id="com.example.app:id/password",
            xpath="//android.widget.EditText[@resource-id='password']",
            platform=self.platform
        )
        
        self.login_button_locators = self.locator_engine.create_smart_locator(
            accessibility_id="login_button",
            text="Login",
            resource_id="com.example.app:id/login_btn",
            platform=self.platform
        )
        
        self.error_message_locators = self.locator_engine.create_smart_locator(
            accessibility_id="error_message",
            resource_id="com.example.app:id/error",
            class_name="android.widget.TextView" if self.is_android else "XCUIElementTypeStaticText",
            platform=self.platform
        )
    
    def enter_username(self, username: str):
        """
        Enter username.
        
        Args:
            username: Username to enter
            
        Returns:
            Self for method chaining
        """
        self.send_keys(self.username_locators, username)
        return self
    
    def enter_password(self, password: str):
        """
        Enter password.
        
        Args:
            password: Password to enter
            
        Returns:
            Self for method chaining
        """
        self.send_keys(self.password_locators, password)
        return self
    
    def click_login(self):
        """
        Click login button.
        
        Returns:
            Self for method chaining
        """
        self.click(self.login_button_locators)
        return self
    
    def login(self, username: str, password: str):
        """
        Perform complete login flow.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            Self for method chaining
        """
        self.enter_username(username).enter_password(password).click_login()
        return self
    
    def get_error_message(self) -> str:
        """
        Get error message text.
        
        Returns:
            Error message or empty string
        """
        try:
            return self.get_text(self.error_message_locators)
        except Exception:
            return ""
    
    def is_error_displayed(self) -> bool:
        """
        Check if error message is displayed.
        
        Returns:
            True if error visible, False otherwise
        """
        return self.is_displayed(self.error_message_locators, timeout=2)


class HomePage(BasePage):
    """Example home page object."""
    
    def __init__(self, driver_wrapper):
        """Initialize home page."""
        super().__init__(driver_wrapper)
        
        # Define locators
        self.welcome_message_locators = self.locator_engine.create_smart_locator(
            accessibility_id="welcome_message",
            resource_id="com.example.app:id/welcome",
            text="Welcome",
            platform=self.platform
        )
        
        self.menu_button_locators = self.locator_engine.create_smart_locator(
            accessibility_id="menu_button",
            resource_id="com.example.app:id/menu",
            class_name="android.widget.ImageButton" if self.is_android else "XCUIElementTypeButton",
            platform=self.platform
        )
        
        self.profile_button_locators = self.locator_engine.create_smart_locator(
            accessibility_id="profile_button",
            text="Profile",
            resource_id="com.example.app:id/profile",
            platform=self.platform
        )
        
        self.settings_button_locators = self.locator_engine.create_smart_locator(
            accessibility_id="settings_button",
            text="Settings",
            resource_id="com.example.app:id/settings",
            platform=self.platform
        )
    
    def is_home_page_displayed(self) -> bool:
        """
        Check if home page is displayed.
        
        Returns:
            True if home page visible, False otherwise
        """
        return self.is_displayed(self.welcome_message_locators)
    
    def get_welcome_message(self) -> str:
        """
        Get welcome message text.
        
        Returns:
            Welcome message text
        """
        return self.get_text(self.welcome_message_locators)
    
    def open_menu(self):
        """
        Open menu.
        
        Returns:
            Self for method chaining
        """
        self.click(self.menu_button_locators)
        return self
    
    def go_to_profile(self):
        """
        Navigate to profile.
        
        Returns:
            Self for method chaining
        """
        self.click(self.profile_button_locators)
        return self
    
    def go_to_settings(self):
        """
        Navigate to settings.
        
        Returns:
            Self for method chaining
        """
        self.click(self.settings_button_locators)
        return self


class SearchPage(BasePage):
    """Example search page object."""
    
    def __init__(self, driver_wrapper):
        """Initialize search page."""
        super().__init__(driver_wrapper)
        
        # Define locators
        self.search_field_locators = self.locator_engine.create_smart_locator(
            accessibility_id="search_field",
            resource_id="com.example.app:id/search",
            class_name="android.widget.EditText" if self.is_android else "XCUIElementTypeSearchField",
            platform=self.platform
        )
        
        self.search_button_locators = self.locator_engine.create_smart_locator(
            accessibility_id="search_button",
            text="Search",
            resource_id="com.example.app:id/search_btn",
            platform=self.platform
        )
        
        self.result_items_locators = self.locator_engine.create_smart_locator(
            resource_id="com.example.app:id/result_item",
            class_name="android.widget.LinearLayout" if self.is_android else "XCUIElementTypeCell",
            xpath="//android.widget.ListView/android.widget.LinearLayout",
            platform=self.platform
        )
    
    def enter_search_query(self, query: str):
        """
        Enter search query.
        
        Args:
            query: Search query text
            
        Returns:
            Self for method chaining
        """
        self.send_keys(self.search_field_locators, query)
        return self
    
    def click_search(self):
        """
        Click search button.
        
        Returns:
            Self for method chaining
        """
        self.click(self.search_button_locators)
        return self
    
    def search(self, query: str):
        """
        Perform complete search.
        
        Args:
            query: Search query text
            
        Returns:
            Self for method chaining
        """
        self.enter_search_query(query).click_search()
        return self
    
    def get_result_count(self) -> int:
        """
        Get number of search results.
        
        Returns:
            Number of results
        """
        elements = self.find_elements(self.result_items_locators, timeout=5)
        return len(elements)
    
    def get_result_at_index(self, index: int) -> str:
        """
        Get text of result at specific index.
        
        Args:
            index: Result index (0-based)
            
        Returns:
            Result text
        """
        elements = self.find_elements(self.result_items_locators)
        if index < len(elements):
            return elements[index].text
        return ""
