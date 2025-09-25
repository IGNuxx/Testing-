



#!/usr/bin/env python3
"""
Test script for TikTok Live Viewer Bot.
"""

import sys
import os
import json

def test_imports():
    """Test that all required modules can be imported."""
    try:
        import selenium
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        print("✓ Selenium imports successful")
        return True
    except ImportError as e:
        print(f"✗ Failed to import selenium: {e}")
        return False

def test_config():
    """Test that configuration file can be loaded."""
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        print("✓ Configuration file loaded successfully")
        print(f"  Max viewers: {config.get('max_viewers', 'N/A')}")
        print(f"  VPN enabled: {config.get('use_vpn', False)}")
        return True
    except Exception as e:
        print(f"✗ Failed to load configuration: {e}")
        return False

def test_accounts():
    """Test account management."""
    try:
        from account_manager import AccountManager
        manager = AccountManager()
        accounts = manager.get_available_accounts()
        print(f"✓ Found {len(accounts)} available accounts")
        if accounts:
            print(f"  Example account: {accounts[0]['username']}")
        return True
    except Exception as e:
        print(f"✗ Failed to load accounts: {e}")
        return False

def main():
    """Run all tests."""
    print("Running TikTok Bot tests...\n")

    tests = [
        test_imports,
        test_config,
        test_accounts
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1

    print(f"\nTest Results: {passed}/{total} tests passed")

    if passed == total:
        print("All tests passed! 🎉")
        return 0
    else:
        print("Some tests failed. 😢")
        return 1

if __name__ == "__main__":
    sys.exit(main())


