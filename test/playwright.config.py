import os


def pytest_configure(config):
    """Configure Playwright for pytest"""
    # Set headed mode by default
    os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", "0")


# Playwright configuration
PLAYWRIGHT_CONFIG = {
    "headless": False,  # Run in headed mode to see what's happening
    "slow_mo": 500,  # Slow down operations by 500ms to see what's happening
    "browser_channel": "chrome",  # Use Chrome browser
    "viewport": {"width": 1280, "height": 720},
    "timeout": 30000,  # 30 second timeout
}
