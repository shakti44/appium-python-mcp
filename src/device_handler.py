"""Device Handler

This module handles device interactions and commands.
"""

import subprocess
from typing import List, Dict, Any, Optional


def list_devices() -> List[Dict[str, str]]:
    """List all connected devices
    
    Returns:
        List of connected devices with their IDs and status
    """
    devices = []
    
    try:
        # Try to list Android devices using adb
        result = subprocess.run(
            ['adb', 'devices'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 2:
                        devices.append({
                            'id': parts[0],
                            'platform': 'Android',
                            'status': parts[1]
                        })
    except (subprocess.TimeoutExpired, FileNotFoundError):
        # adb not available or timeout
        pass
    
    # TODO: Add iOS device listing using idevice_id when available
    
    return devices


def send_command(device_id: str, command: str) -> Dict[str, Any]:
    """Send a command to the specified device
    
    Args:
        device_id: The device identifier
        command: Command to execute
        
    Returns:
        Dictionary containing command result
    """
    try:
        # Execute adb command for Android devices
        result = subprocess.run(
            ['adb', '-s', device_id, 'shell', command],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return {
            'device_id': device_id,
            'command': command,
            'returncode': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'success': result.returncode == 0
        }
    except subprocess.TimeoutExpired:
        return {
            'device_id': device_id,
            'command': command,
            'error': 'Command timeout',
            'success': False
        }
    except FileNotFoundError:
        return {
            'device_id': device_id,
            'command': command,
            'error': 'adb not found',
            'success': False
        }
    except Exception as e:
        return {
            'device_id': device_id,
            'command': command,
            'error': str(e),
            'success': False
        }


def get_device_status(device_id: str) -> Optional[Dict[str, Any]]:
    """Get the status of the specified device
    
    Args:
        device_id: The device identifier
        
    Returns:
        Dictionary containing device status or None if not found
    """
    devices = list_devices()
    
    for device in devices:
        if device['id'] == device_id:
            # Get additional device info
            try:
                # Get device model
                model_result = subprocess.run(
                    ['adb', '-s', device_id, 'shell', 'getprop', 'ro.product.model'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                # Get Android version
                version_result = subprocess.run(
                    ['adb', '-s', device_id, 'shell', 'getprop', 'ro.build.version.release'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                device['model'] = model_result.stdout.strip() if model_result.returncode == 0 else 'Unknown'
                device['android_version'] = version_result.stdout.strip() if version_result.returncode == 0 else 'Unknown'
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
            
            return device
    
    return None

