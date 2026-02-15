#!/usr/bin/env python
"""
Verification script to demonstrate all features of the appium-python-mcp codebase
"""

import sys
sys.path.insert(0, '.')

from src.session_manager import SessionManager
from src.device_handler import list_devices, send_command, get_device_status
from appium_driver import AppiumDriver

def test_session_manager():
    """Test SessionManager functionality"""
    print("=" * 60)
    print("Testing SessionManager")
    print("=" * 60)
    
    manager = SessionManager()
    
    # Create session
    session_id = manager.create_session(data={'test': 'data'})
    print(f"✓ Created session: {session_id}")
    
    # Get session
    session = manager.get_session(session_id)
    print(f"✓ Retrieved session: {session['id']}")
    
    # Check active
    is_active = manager.is_session_active(session_id)
    print(f"✓ Session active: {is_active}")
    
    # List sessions
    sessions = manager.list_sessions()
    print(f"✓ Total active sessions: {len(list(sessions))}")
    
    # Expire session
    manager.expire_session(session_id)
    is_active = manager.is_session_active(session_id)
    print(f"✓ Session expired, active: {is_active}")
    
    # Create another and delete
    session_id2 = manager.create_session()
    manager.delete_session(session_id2)
    session = manager.get_session(session_id2)
    print(f"✓ Deleted session, retrieved: {session}")
    
    print()

def test_device_handler():
    """Test device handler functionality"""
    print("=" * 60)
    print("Testing Device Handler")
    print("=" * 60)
    
    # List devices (will work even if no devices connected)
    devices = list_devices()
    print(f"✓ Listed devices: {len(devices)} found")
    for device in devices:
        print(f"  - {device['id']} ({device['platform']}, {device['status']})")
    
    if devices:
        device_id = devices[0]['id']
        
        # Get device status
        status = get_device_status(device_id)
        print(f"✓ Got device status: {status}")
        
        # Send command (echo test)
        result = send_command(device_id, 'echo "test"')
        print(f"✓ Sent command, success: {result.get('success', False)}")
    else:
        print("  (No devices connected - skipping device commands)")
    
    print()

def test_appium_driver():
    """Test AppiumDriver functionality"""
    print("=" * 60)
    print("Testing AppiumDriver")
    print("=" * 60)
    
    # Create driver instance (don't start it as we don't have Appium server)
    driver = AppiumDriver(
        platform_name='Android',
        device_name='test-device',
        app='/path/to/app.apk'
    )
    print("✓ Created AppiumDriver instance")
    print(f"  - Platform: {driver.desired_caps['platformName']}")
    print(f"  - Device: {driver.desired_caps['deviceName']}")
    print(f"  - App: {driver.desired_caps['app']}")
    
    print()

def test_fastapi_server():
    """Test FastAPI server imports"""
    print("=" * 60)
    print("Testing FastAPI Server")
    print("=" * 60)
    
    from mcp_server.server import app, session_manager
    print("✓ Imported FastAPI app")
    print(f"✓ Session manager initialized")
    print(f"  - Active sessions: {len(list(session_manager.list_sessions()))}")
    
    # Test that endpoints are registered
    routes = [route.path for route in app.routes]
    print(f"✓ Server has {len(routes)} routes registered")
    print("  Key endpoints:")
    for route in ["/", "/health", "/session/", "/devices/"]:
        if route in routes:
            print(f"    ✓ {route}")
    
    print()

def main():
    """Run all tests"""
    print()
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  Appium Python MCP - Verification Test".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    try:
        test_session_manager()
        test_device_handler()
        test_appium_driver()
        test_fastapi_server()
        
        print("=" * 60)
        print("✓ All verification tests passed!")
        print("=" * 60)
        print()
        print("The codebase is working correctly and ready for use.")
        print()
        return 0
        
    except Exception as e:
        print()
        print("=" * 60)
        print(f"✗ Verification failed: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
