from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait


class AssertHelper:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def title_equals(self, expected: str, timeout=30):
        WebDriverWait(self.driver, timeout).until(EC.title_is(expected))
        assert self.driver.title == expected, (
            f"Title sai | Expected: '{expected}' | Actual: '{self.driver.title}'"
        )

    def element_visible(self, locator, timeout=10):
        # locator dạng (By.XPATH, "...")
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator),
            message=f"Element không hiển thị: {locator}"
        )
        assert element.is_displayed(), f"Element không hiển thị: {locator}"
        return element

    def element_text_contains(self, element: WebElement, expected: str):
        actual = element.text
        assert expected in actual, f"Text không khớp | Expected chứa: '{expected}' | Actual: '{actual}'"

    def element_attribute_equals(self, element: WebElement, attr: str, expected: str):
        actual = element.get_attribute(attr)
        assert actual == expected, f" Attribute '{attr}' sai | Expected: '{expected}' | Actual: '{actual}'"