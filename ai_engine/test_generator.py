"""Test generator for creating automated test cases."""
from typing import List, Optional, Dict, Any
from datetime import datetime
from ai_engine.nlp_processor import ParsedCommand
from utils.logger import logger


class TestGenerator:
    """Generator for creating pytest test cases from commands."""
    
    def __init__(self):
        """Initialize test generator."""
        self.logger = logger
    
    def generate_test_from_commands(
        self,
        test_name: str,
        commands: List[ParsedCommand],
        description: Optional[str] = None,
        platform: str = "Android"
    ) -> str:
        """
        Generate pytest test case from command list.
        
        Args:
            test_name: Name of the test
            commands: List of ParsedCommand objects
            description: Optional test description
            platform: Target platform
            
        Returns:
            Generated test code as string
        """
        self.logger.info(f"Generating test: {test_name}")
        
        # Sanitize test name
        test_func_name = test_name.lower().replace(' ', '_').replace('-', '_')
        test_func_name = f"test_{test_func_name}"
        
        # Generate imports
        imports = self._generate_imports()
        
        # Generate test function
        test_code = self._generate_test_function(
            test_func_name,
            commands,
            description,
            platform
        )
        
        full_code = f"{imports}\n\n{test_code}"
        
        return full_code
    
    def _generate_imports(self) -> str:
        """Generate import statements."""
        return """import pytest
from appium_driver.driver import AppiumDriverWrapper
from ai_engine.command_parser import CommandParser
from ai_engine.nlp_processor import ParsedCommand"""
    
    def _generate_test_function(
        self,
        func_name: str,
        commands: List[ParsedCommand],
        description: Optional[str],
        platform: str
    ) -> str:
        """Generate test function code."""
        # Generate docstring
        docstring = f'    """{description or func_name}"""'
        
        # Generate test steps
        steps = []
        for i, cmd in enumerate(commands):
            step_code = self._generate_command_code(cmd, i + 1)
            steps.append(step_code)
        
        steps_code = '\n    '.join(steps)
        
        test_code = f"""
@pytest.mark.integration
def {func_name}(driver_wrapper):
{docstring}
    parser = CommandParser(driver_wrapper)
    
    # Execute test steps
    {steps_code}
"""
        
        return test_code
    
    def _generate_command_code(self, command: ParsedCommand, step_num: int) -> str:
        """Generate code for a single command."""
        # Create comment
        comment = f"# Step {step_num}: {command.action}"
        if command.target:
            comment += f" on {command.target}"
        if command.value:
            comment += f" with '{command.value}'"
        
        # Create command object
        params_str = "{" + ", ".join(f"'{k}': {repr(v)}" for k, v in command.params.items()) + "}"
        
        cmd_str = f"""cmd = ParsedCommand(
        action='{command.action}',
        target={repr(command.target)},
        value={repr(command.value)},
        params={params_str}
    )
    parser.execute_command(cmd)"""
        
        return f"{comment}\n    {cmd_str}"
    
    def generate_page_object(
        self,
        page_name: str,
        elements: List[Dict[str, str]],
        platform: str = "Android"
    ) -> str:
        """
        Generate Page Object class.
        
        Args:
            page_name: Name of the page
            elements: List of element definitions
            platform: Target platform
            
        Returns:
            Generated Page Object code
        """
        self.logger.info(f"Generating page object: {page_name}")
        
        # Sanitize class name
        class_name = ''.join(word.capitalize() for word in page_name.split())
        if not class_name.endswith('Page'):
            class_name += 'Page'
        
        # Generate imports
        imports = """from page_objects.base_page import BasePage
from locators.strategy import LocatorStrategy"""
        
        # Generate class
        class_code = self._generate_page_class(class_name, elements, platform)
        
        return f"{imports}\n\n\n{class_code}"
    
    def _generate_page_class(
        self,
        class_name: str,
        elements: List[Dict[str, str]],
        platform: str
    ) -> str:
        """Generate page class code."""
        # Generate __init__ method with locators
        locators_code = []
        for elem in elements:
            name = elem.get('name', 'element')
            locator_name = f"{name}_locators"
            
            locator_def = f"""self.{locator_name} = self.locator_engine.create_smart_locator(
            accessibility_id="{elem.get('accessibility_id', '')}",
            resource_id="{elem.get('resource_id', '')}",
            text="{elem.get('text', '')}",
            platform=self.platform
        )"""
            
            locators_code.append(f"        {locator_def}")
        
        locators_str = '\n        \n'.join(locators_code)
        
        # Generate action methods
        methods = []
        for elem in elements:
            name = elem.get('name', 'element')
            method = self._generate_element_method(name)
            methods.append(method)
        
        methods_str = '\n    \n'.join(methods)
        
        class_code = f'''class {class_name}(BasePage):
    """Generated page object for {class_name}."""
    
    def __init__(self, driver_wrapper):
        """Initialize {class_name}."""
        super().__init__(driver_wrapper)
        
        # Define locators
{locators_str}
    
{methods_str}
'''
        
        return class_code
    
    def _generate_element_method(self, element_name: str) -> str:
        """Generate method for element interaction."""
        method_name = f"click_{element_name}"
        locator_name = f"{element_name}_locators"
        
        return f'''    def {method_name}(self):
        """
        Click {element_name}.
        
        Returns:
            Self for method chaining
        """
        self.click(self.{locator_name})
        return self
    
    def get_{element_name}_text(self) -> str:
        """
        Get text from {element_name}.
        
        Returns:
            Element text
        """
        return self.get_text(self.{locator_name})
    
    def is_{element_name}_displayed(self) -> bool:
        """
        Check if {element_name} is displayed.
        
        Returns:
            True if displayed, False otherwise
        """
        return self.is_displayed(self.{locator_name})'''
    
    def generate_test_suite(
        self,
        suite_name: str,
        test_cases: List[Dict[str, Any]]
    ) -> str:
        """
        Generate complete test suite file.
        
        Args:
            suite_name: Name of the test suite
            test_cases: List of test case definitions
            
        Returns:
            Generated test suite code
        """
        self.logger.info(f"Generating test suite: {suite_name}")
        
        # Generate header
        header = f'''"""
Test suite: {suite_name}
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
'''
        
        # Generate imports
        imports = self._generate_imports()
        
        # Generate each test
        tests = []
        for test_case in test_cases:
            test_name = test_case.get('name', 'unnamed_test')
            commands = test_case.get('commands', [])
            description = test_case.get('description')
            platform = test_case.get('platform', 'Android')
            
            test_code = self._generate_test_function(
                test_name,
                commands,
                description,
                platform
            )
            tests.append(test_code)
        
        tests_str = '\n\n'.join(tests)
        
        return f"{header}\n{imports}\n{tests_str}"
    
    def save_test_to_file(self, test_code: str, filepath: str):
        """
        Save generated test to file.
        
        Args:
            test_code: Generated test code
            filepath: Path to save file
        """
        with open(filepath, 'w') as f:
            f.write(test_code)
        
        self.logger.info(f"Test saved to: {filepath}")
    
    def save_page_object_to_file(self, page_code: str, filepath: str):
        """
        Save generated page object to file.
        
        Args:
            page_code: Generated page object code
            filepath: Path to save file
        """
        with open(filepath, 'w') as f:
            f.write(page_code)
        
        self.logger.info(f"Page object saved to: {filepath}")
