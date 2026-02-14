"""NLP processor for natural language command processing."""
import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from utils.logger import logger


@dataclass
class ParsedCommand:
    """Parsed command structure."""
    action: str
    target: Optional[str] = None
    value: Optional[str] = None
    params: Dict[str, Any] = None
    confidence: float = 1.0
    
    def __post_init__(self):
        if self.params is None:
            self.params = {}


class NLPProcessor:
    """Natural language processor for mobile automation commands."""
    
    # Action keywords mapping
    ACTION_KEYWORDS = {
        'click': ['click', 'tap', 'press', 'select', 'choose'],
        'type': ['type', 'enter', 'input', 'write', 'fill'],
        'swipe': ['swipe', 'scroll', 'slide', 'drag'],
        'wait': ['wait', 'pause', 'delay'],
        'verify': ['verify', 'check', 'assert', 'confirm', 'validate'],
        'open': ['open', 'launch', 'start'],
        'close': ['close', 'exit', 'quit'],
        'navigate': ['navigate', 'go to', 'goto', 'move to'],
        'back': ['back', 'go back', 'return'],
        'screenshot': ['screenshot', 'capture', 'take picture'],
        'get': ['get', 'retrieve', 'fetch', 'read'],
        'find': ['find', 'locate', 'search for'],
    }
    
    # Direction keywords
    DIRECTIONS = {
        'up': ['up', 'upward', 'upwards'],
        'down': ['down', 'downward', 'downwards'],
        'left': ['left', 'leftward'],
        'right': ['right', 'rightward'],
    }
    
    def __init__(self):
        """Initialize NLP processor."""
        self.logger = logger
    
    def parse_command(self, command: str) -> ParsedCommand:
        """
        Parse natural language command.
        
        Args:
            command: Natural language command string
            
        Returns:
            ParsedCommand object
        """
        command = command.lower().strip()
        self.logger.debug(f"Parsing command: {command}")
        
        # Try to match action
        action = self._extract_action(command)
        
        # Extract target element
        target = self._extract_target(command)
        
        # Extract value (for type commands)
        value = self._extract_value(command, action)
        
        # Extract parameters
        params = self._extract_params(command, action)
        
        parsed = ParsedCommand(
            action=action,
            target=target,
            value=value,
            params=params
        )
        
        self.logger.info(f"Parsed command: action={action}, target={target}, value={value}")
        return parsed
    
    def _extract_action(self, command: str) -> str:
        """Extract action from command."""
        for action, keywords in self.ACTION_KEYWORDS.items():
            for keyword in keywords:
                if keyword in command:
                    return action
        
        # Default to click if no action found
        return 'click'
    
    def _extract_target(self, command: str) -> Optional[str]:
        """Extract target element from command."""
        # Look for quoted text
        quoted = re.findall(r'"([^"]+)"', command)
        if quoted:
            return quoted[0]
        
        quoted = re.findall(r"'([^']+)'", command)
        if quoted:
            return quoted[0]
        
        # Look for "button", "field", "element" patterns
        patterns = [
            r'(?:button|field|element|text|link|image)\s+(?:called|named|labeled|with\s+text)?\s*["\']?(\w+)["\']?',
            r'(?:the\s+)?(\w+)\s+(?:button|field|element)',
            r'on\s+(?:the\s+)?(\w+)',
            r'to\s+(?:the\s+)?(\w+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, command)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_value(self, command: str, action: str) -> Optional[str]:
        """Extract value from command (for type actions)."""
        if action != 'type':
            return None
        
        # Look for value after "with", "as", "text"
        patterns = [
            r'with\s+["\']([^"\']+)["\']',
            r'as\s+["\']([^"\']+)["\']',
            r'text\s+["\']([^"\']+)["\']',
            r'value\s+["\']([^"\']+)["\']',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, command)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_params(self, command: str, action: str) -> Dict[str, Any]:
        """Extract parameters from command."""
        params = {}
        
        # Extract direction for swipe/scroll
        if action == 'swipe':
            for direction, keywords in self.DIRECTIONS.items():
                for keyword in keywords:
                    if keyword in command:
                        params['direction'] = direction
                        break
        
        # Extract duration/timeout
        duration_match = re.search(r'(?:for|duration|wait)\s+(\d+)\s*(?:seconds?|secs?|s)?', command)
        if duration_match:
            params['duration'] = int(duration_match.group(1)) * 1000  # Convert to ms
        
        # Extract count (for multiple taps)
        count_match = re.search(r'(\d+)\s+times?', command)
        if count_match:
            params['count'] = int(count_match.group(1))
        
        return params
    
    def suggest_actions(self, partial_command: str) -> List[str]:
        """
        Suggest possible actions based on partial command.
        
        Args:
            partial_command: Partial command string
            
        Returns:
            List of suggested complete commands
        """
        suggestions = []
        partial = partial_command.lower()
        
        # Check which actions match
        for action, keywords in self.ACTION_KEYWORDS.items():
            for keyword in keywords:
                if keyword.startswith(partial) or partial in keyword:
                    suggestions.append(f"{keyword} on element")
        
        return suggestions[:5]  # Return top 5 suggestions
    
    def validate_command(self, command: str) -> tuple[bool, Optional[str]]:
        """
        Validate if command can be parsed.
        
        Args:
            command: Command to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not command or len(command.strip()) == 0:
            return False, "Command cannot be empty"
        
        parsed = self.parse_command(command)
        
        if not parsed.action:
            return False, "No valid action found in command"
        
        # Some actions require a target
        if parsed.action in ['click', 'type', 'verify'] and not parsed.target:
            return False, f"Action '{parsed.action}' requires a target element"
        
        # Type action requires a value
        if parsed.action == 'type' and not parsed.value:
            return False, "Type action requires a value to enter"
        
        return True, None
    
    def extract_test_steps(self, test_description: str) -> List[ParsedCommand]:
        """
        Extract test steps from a test description.
        
        Args:
            test_description: Multi-line test description
            
        Returns:
            List of ParsedCommand objects
        """
        steps = []
        
        # Split by newlines and numbered lists
        lines = test_description.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#') or line.startswith('//'):
                continue
            
            # Remove numbering (1., 2., etc.)
            line = re.sub(r'^\d+[\.)]\s*', '', line)
            
            # Remove bullet points
            line = re.sub(r'^[-*•]\s*', '', line)
            
            if line:
                try:
                    parsed = self.parse_command(line)
                    steps.append(parsed)
                except Exception as e:
                    self.logger.warning(f"Failed to parse step: {line} - {e}")
        
        return steps
