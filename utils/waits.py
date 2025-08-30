from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DEFAULT_TIMEOUT = 10

def wait_for_visible(driver, locator, timeout=DEFAULT_TIMEOUT):
    """Chờ cho element hiển thị (visible)"""
    try:
        return WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
    except TimeoutException:
        print(f"[wait_for_visible] Hết {timeout}s nhưng không thấy element: {locator}")
        return None


def wait_for_clickable(driver, locator, timeout=DEFAULT_TIMEOUT):
    """Chờ cho element có thể click"""
    try:
        return WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
    except TimeoutException:
        print(f"[wait_for_clickable] Hết {timeout}s nhưng element không clickable: {locator}")
        return None


def wait_for_presence(driver, locator, timeout=DEFAULT_TIMEOUT):
    """Chờ cho element có trong DOM (chưa chắc nhìn thấy)"""
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
    except TimeoutException:
        print(f"[wait_for_presence] Hết {timeout}s nhưng không tìm thấy element trong DOM: {locator}")
        return None