from selenium.webdriver.common.by import By

from utils.waits import wait_for_visible


class ConfigPage:
    def __init__(self,driver):
        self.driver = driver
        self.header = (By.CSS_SELECTOR, "h1.page-title")

    def is_loaded(self):
        header = wait_for_visible(self.driver, self.header)
        return "Khai báo tham số hệ thống" in header.text

