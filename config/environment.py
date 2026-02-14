"""Environment configuration management."""
import os
import json
from pathlib import Path
from typing import Optional, Dict, Any
from pydantic import Field
from pydantic_settings import BaseSettings
import yaml


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Server configuration
    server_host: str = Field(default="0.0.0.0", env="SERVER_HOST")
    server_port: int = Field(default=8080, env="SERVER_PORT")
    
    # Appium configuration
    appium_server_url: str = Field(default="http://localhost:4723", env="APPIUM_SERVER_URL")
    implicit_wait: int = Field(default=10, env="IMPLICIT_WAIT")
    explicit_wait: int = Field(default=30, env="EXPLICIT_WAIT")
    
    # AI/NLP configuration
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    ai_model: str = Field(default="gpt-4", env="AI_MODEL")
    
    # Test configuration
    screenshot_on_failure: bool = Field(default=True, env="SCREENSHOT_ON_FAILURE")
    video_recording: bool = Field(default=False, env="VIDEO_RECORDING")
    
    # Logging configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: Optional[str] = Field(default=None, env="LOG_FILE")
    
    # Report configuration
    report_dir: str = Field(default="reports", env="REPORT_DIR")
    screenshot_dir: str = Field(default="screenshots", env="SCREENSHOT_DIR")
    
    # Platform defaults
    default_platform: str = Field(default="Android", env="DEFAULT_PLATFORM")
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


class ConfigManager:
    """Configuration manager for loading capabilities and device configs."""
    
    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_dir: Directory containing config files
        """
        self.config_dir = config_dir or Path(__file__).parent
        self.capabilities_file = self.config_dir / "capabilities.json"
        self.devices_file = self.config_dir / "devices.yaml"
    
    def load_capabilities(self, platform: Optional[str] = None) -> Dict[str, Any]:
        """
        Load capabilities from JSON file.
        
        Args:
            platform: Platform name (android, ios, etc.)
            
        Returns:
            Capabilities dictionary
        """
        if not self.capabilities_file.exists():
            raise FileNotFoundError(f"Capabilities file not found: {self.capabilities_file}")
        
        with open(self.capabilities_file, 'r') as f:
            all_caps = json.load(f)
        
        if platform:
            platform_lower = platform.lower()
            if platform_lower in all_caps:
                return all_caps[platform_lower]
            raise ValueError(f"Platform '{platform}' not found in capabilities file")
        
        return all_caps
    
    def load_devices(self) -> Dict[str, Any]:
        """
        Load device configurations from YAML file.
        
        Returns:
            Device configuration dictionary
        """
        if not self.devices_file.exists():
            raise FileNotFoundError(f"Devices file not found: {self.devices_file}")
        
        with open(self.devices_file, 'r') as f:
            return yaml.safe_load(f)
    
    def merge_capabilities(
        self,
        base_caps: Dict[str, Any],
        override_caps: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Merge base capabilities with overrides.
        
        Args:
            base_caps: Base capabilities
            override_caps: Override capabilities
            
        Returns:
            Merged capabilities
        """
        merged = base_caps.copy()
        if override_caps:
            merged.update(override_caps)
        return merged


# Global settings instance
settings = Settings()

# Global config manager instance
config_manager = ConfigManager()
