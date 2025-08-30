from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AuthHelper:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.span_agent_name_user = (By.ID, "span_agent_name_user")
        self.span_full_name_home_page = (By.ID, "spanFullNameHomePage")

    def switch_account(self, account_name):
        # Hover vào user menu
        span_user = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.span_agent_name_user)
        )
        ActionChains(self.driver).move_to_element(span_user).perform()

        # Locator menu item (normalize-space để bỏ khoảng trắng thừa)
        menu_item_locator = (
            By.XPATH,
            f"//a[@role='menuitem' and contains(normalize-space(.), '{account_name.strip()}')]"
        )

        # Chờ menu item hiển thị và clickable
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(menu_item_locator)
        ).click()

        # Chờ đổi account thành công (spanFullNameHomePage đổi text)
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element(self.span_full_name_home_page, account_name)
        )