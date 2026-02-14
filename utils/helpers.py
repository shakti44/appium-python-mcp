"""Helper utilities for automation."""
import time
import functools
from typing import Callable, Any, Optional, TypeVar
from utils.logger import logger

T = TypeVar('T')


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,)
) -> Callable:
    """
    Retry decorator with exponential backoff.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Multiplier for delay after each retry
        exceptions: Tuple of exceptions to catch
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            current_delay = delay
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(
                            f"Attempt {attempt + 1}/{max_attempts} failed for {func.__name__}: {e}. "
                            f"Retrying in {current_delay}s..."
                        )
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        logger.error(f"All {max_attempts} attempts failed for {func.__name__}")
            
            raise last_exception
        
        return wrapper
    return decorator


def wait_until(
    condition: Callable[[], bool],
    timeout: float = 10.0,
    poll_interval: float = 0.5,
    error_message: Optional[str] = None
) -> bool:
    """
    Wait until a condition becomes true or timeout occurs.
    
    Args:
        condition: Callable that returns boolean
        timeout: Maximum time to wait in seconds
        poll_interval: Time between condition checks in seconds
        error_message: Optional custom error message
        
    Returns:
        True if condition met, raises TimeoutError otherwise
    """
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            if condition():
                return True
        except Exception as e:
            logger.debug(f"Condition check raised exception: {e}")
        
        time.sleep(poll_interval)
    
    msg = error_message or f"Condition not met within {timeout}s"
    logger.error(msg)
    raise TimeoutError(msg)


def safe_get(dictionary: dict, *keys: str, default: Any = None) -> Any:
    """
    Safely get nested dictionary value.
    
    Args:
        dictionary: Dictionary to query
        keys: Keys to traverse
        default: Default value if key not found
        
    Returns:
        Value if found, default otherwise
    """
    result = dictionary
    for key in keys:
        if isinstance(result, dict):
            result = result.get(key)
            if result is None:
                return default
        else:
            return default
    return result


def merge_dicts(*dicts: dict) -> dict:
    """
    Merge multiple dictionaries.
    
    Args:
        dicts: Dictionaries to merge
        
    Returns:
        Merged dictionary
    """
    result = {}
    for d in dicts:
        if d:
            result.update(d)
    return result


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate string to maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix
